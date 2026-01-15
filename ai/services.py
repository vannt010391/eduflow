"""
AI service layer for EduFlow AI

This module handles all AI API calls with proper error handling,
caching, logging, and fallback mechanisms.

Design Principles:
- Event-based, not continuous
- Cached per event unless user regenerates
- Logged with input/output for debugging
- Falls back to deterministic scheduling on failure
"""
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from django.core.cache import cache
from django.conf import settings

from .schemas import (
    validate_learning_plan,
    validate_learning_task,
    LearningPlan,
    ReplanSuggestion
)

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Raised when AI service fails"""
    pass


class AIService:
    """
    Main AI service for generating learning plans and suggestions.

    This service abstracts the AI provider (OpenAI, Anthropic, etc.)
    and provides a consistent interface for the application.
    """

    def __init__(self):
        """
        Initialize AI service with provider configuration.

        Supports multiple AI providers:
        - 'openai': OpenAI GPT models
        - 'anthropic': Anthropic Claude models
        - 'mock': Mock responses for testing
        """
        self.provider = getattr(settings, 'AI_PROVIDER', 'mock')
        self.api_key = getattr(settings, 'AI_API_KEY', None)
        self.model = getattr(settings, 'AI_MODEL', 'gpt-4')
        self.enabled = getattr(settings, 'AI_ENABLED', False)

        if self.enabled and self.provider != 'mock' and not self.api_key:
            logger.warning("AI enabled but no API key configured")

    def generate_learning_plan(
        self,
        event_title: str,
        event_type: str,
        event_date: datetime,
        prep_time_hours: float,
        subject: str,
        description: str,
        daily_limit_minutes: int = 480,
        focus_mode: str = "Pomodoro",
        force_regenerate: bool = False
    ) -> Optional[LearningPlan]:
        """
        Generate a learning plan for an event.

        This implements AI Use Case #1: Event → Learning Plan Generation

        Args:
            event_title: Title of the event
            event_type: Type (exam, quiz, assignment, etc.)
            event_date: When the event occurs
            prep_time_hours: Total hours available for preparation
            subject: Subject/topic
            description: User's description of what to study
            daily_limit_minutes: User's daily study limit
            focus_mode: User's preferred focus mode
            force_regenerate: Skip cache and regenerate

        Returns:
            LearningPlan dict or None if AI fails
        """
        # Generate cache key
        cache_key = f"ai_plan_{event_title}_{event_date.isoformat()}_{prep_time_hours}"

        # Check cache unless forced regeneration
        if not force_regenerate:
            cached_plan = cache.get(cache_key)
            if cached_plan:
                logger.info(f"Returning cached plan for: {event_title}")
                return cached_plan

        # Check if AI is enabled
        if not self.enabled:
            logger.info("AI is disabled, skipping plan generation")
            return None

        try:
            # Load prompt template
            prompt = self._load_prompt_template('plan_generation.txt')

            # Format prompt with event data
            formatted_prompt = prompt.format(
                event_title=event_title,
                event_type=event_type,
                event_date=event_date.strftime('%Y-%m-%d'),
                prep_time_hours=prep_time_hours,
                subject=subject,
                description=description or "No additional details provided",
                daily_limit_minutes=daily_limit_minutes,
                focus_mode=focus_mode
            )

            # Call AI provider
            response = self._call_ai_provider(formatted_prompt)

            # Parse and validate response
            plan = self._parse_json_response(response)
            validate_learning_plan(plan)

            # Log successful generation
            logger.info(
                f"Generated learning plan for '{event_title}': "
                f"{len(plan['tasks'])} tasks, "
                f"~{sum(t['suggested_duration_minutes'] for t in plan['tasks'])} minutes"
            )

            # Cache the result (24 hours)
            cache.set(cache_key, plan, timeout=86400)

            return plan

        except Exception as e:
            logger.error(f"AI plan generation failed: {str(e)}", exc_info=True)
            return None

    def suggest_replan(
        self,
        event_title: str,
        tasks_data: List[Dict],
        issue_type: str,
        performance_data: Dict
    ) -> Optional[ReplanSuggestion]:
        """
        Generate adaptive re-planning suggestions.

        This implements AI Use Case #3: Adaptive Re-Planning

        Args:
            event_title: Title of the event
            tasks_data: List of current tasks with performance data
            issue_type: Type of issue detected (tasks_overrunning, etc.)
            performance_data: Performance metrics

        Returns:
            ReplanSuggestion dict or None if AI fails
        """
        if not self.enabled:
            logger.info("AI is disabled, skipping replan suggestions")
            return None

        try:
            # Load prompt template
            prompt = self._load_prompt_template('replanning.txt')

            # Build issue description
            issue_descriptions = {
                'tasks_overrunning': f"User is taking {performance_data.get('avg_overrun_percent', 0)}% longer than estimated on tasks",
                'tasks_skipped': f"User has skipped {performance_data.get('skipped_count', 0)} tasks",
                'event_at_risk': f"Event is {performance_data.get('completion_percent', 0)}% complete with {performance_data.get('days_remaining', 0)} days left"
            }

            # Format prompt
            formatted_prompt = prompt.format(
                event_title=event_title,
                tasks_data=json.dumps(tasks_data, indent=2),
                issue_type=issue_type,
                performance_data=json.dumps(performance_data, indent=2),
                issue_description=issue_descriptions.get(issue_type, "Unknown issue")
            )

            # Call AI provider
            response = self._call_ai_provider(formatted_prompt)

            # Parse response
            suggestion = self._parse_json_response(response)

            # Log suggestion
            logger.info(
                f"Generated replan suggestion for '{event_title}': "
                f"{len(suggestion.get('suggestions', []))} suggestions"
            )

            return suggestion

        except Exception as e:
            logger.error(f"AI replan suggestion failed: {str(e)}", exc_info=True)
            return None

    def _load_prompt_template(self, filename: str) -> str:
        """Load a prompt template from the prompts directory."""
        import os
        from django.conf import settings

        prompt_path = os.path.join(settings.BASE_DIR, 'ai', 'prompts', filename)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _call_ai_provider(self, prompt: str) -> str:
        """
        Call the configured AI provider with the prompt.

        Args:
            prompt: Formatted prompt text

        Returns:
            AI response text

        Raises:
            AIServiceError: If AI call fails
        """
        if self.provider == 'mock':
            return self._mock_response(prompt)
        elif self.provider == 'openai':
            return self._call_openai(prompt)
        elif self.provider == 'anthropic':
            return self._call_anthropic(prompt)
        else:
            raise AIServiceError(f"Unknown AI provider: {self.provider}")

    def _mock_response(self, prompt: str) -> str:
        """
        Generate mock response for testing.

        Returns a valid learning plan JSON.
        """
        # Detect which prompt type based on content
        if 'Event Title:' in prompt and 'Total Preparation Time' in prompt:
            # Plan generation
            return json.dumps({
                "goal_summary": "Study plan generated by mock AI service",
                "tasks": [
                    {
                        "title": "Review key concepts and fundamentals",
                        "task_type": "concept_review",
                        "suggested_duration_minutes": 30,
                        "difficulty": "low",
                        "cognitive_load": "medium",
                        "notes": "Start with understanding core principles"
                    },
                    {
                        "title": "Practice problems and exercises",
                        "task_type": "practice",
                        "suggested_duration_minutes": 45,
                        "difficulty": "medium",
                        "cognitive_load": "high",
                        "notes": "Apply concepts through problem-solving"
                    },
                    {
                        "title": "Deep practice: Complex scenarios",
                        "task_type": "deep_practice",
                        "suggested_duration_minutes": 45,
                        "difficulty": "high",
                        "cognitive_load": "high",
                        "notes": "Challenge yourself with difficult problems"
                    },
                    {
                        "title": "Revision and review",
                        "task_type": "revision",
                        "suggested_duration_minutes": 30,
                        "difficulty": "low",
                        "cognitive_load": "low",
                        "notes": "Consolidate learning and fill gaps"
                    }
                ]
            })
        else:
            # Replan suggestion
            return json.dumps({
                "issue_detected": "tasks_overrunning",
                "suggestions": [
                    {
                        "action": "split_task",
                        "task_title": "Practice problems and exercises",
                        "new_duration_minutes": 30,
                        "reason": "Break into smaller chunks to match actual pace"
                    }
                ]
            })

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        try:
            import openai
            openai.api_key = self.api_key

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an educational planning assistant. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            raise AIServiceError(f"OpenAI API call failed: {str(e)}")

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text

        except Exception as e:
            raise AIServiceError(f"Anthropic API call failed: {str(e)}")

    def _parse_json_response(self, response: str) -> Dict:
        """
        Parse JSON from AI response, handling markdown code blocks.

        Args:
            response: Raw AI response text

        Returns:
            Parsed JSON dict

        Raises:
            AIServiceError: If JSON parsing fails
        """
        # Remove markdown code blocks if present
        response = response.strip()
        if response.startswith('```json'):
            response = response[7:]
        elif response.startswith('```'):
            response = response[3:]

        if response.endswith('```'):
            response = response[:-3]

        response = response.strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise AIServiceError(f"Failed to parse JSON response: {str(e)}\nResponse: {response}")


# Global service instance
_ai_service = None


def get_ai_service() -> AIService:
    """
    Get the global AI service instance.

    Returns:
        AIService singleton
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
