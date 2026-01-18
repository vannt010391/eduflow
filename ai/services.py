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
    validate_diagnostic_analysis,
    validate_plan_adjustment,
    LearningPlan,
    ReplanSuggestion,
    DiagnosticAnalysisResult,
    PlanAdjustmentResult
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

        Returns a valid learning plan JSON with multiple balanced tasks.
        """
        # Detect which prompt type based on content
        if 'Event Title:' in prompt and 'Total Preparation Time' in prompt:
            # Plan generation with more balanced tasks (10+ tasks for 6 hours)
            return json.dumps({
                "goal_summary": "Comprehensive study plan with balanced, focused tasks",
                "tasks": [
                    {
                        "title": "Review fundamental concepts - Part 1",
                        "task_type": "concept_review",
                        "suggested_duration_minutes": 30,
                        "difficulty": "low",
                        "cognitive_load": "medium",
                        "notes": "Focus on basic terminology and definitions"
                    },
                    {
                        "title": "Review fundamental concepts - Part 2",
                        "task_type": "concept_review",
                        "suggested_duration_minutes": 30,
                        "difficulty": "low",
                        "cognitive_load": "medium",
                        "notes": "Focus on key principles and theories"
                    },
                    {
                        "title": "Practice: Basic problems",
                        "task_type": "practice",
                        "suggested_duration_minutes": 30,
                        "difficulty": "low",
                        "cognitive_load": "medium",
                        "notes": "Start with simple exercises to build confidence"
                    },
                    {
                        "title": "Practice: Intermediate problems - Set 1",
                        "task_type": "practice",
                        "suggested_duration_minutes": 30,
                        "difficulty": "medium",
                        "cognitive_load": "high",
                        "notes": "Apply concepts to moderate difficulty problems"
                    },
                    {
                        "title": "Practice: Intermediate problems - Set 2",
                        "task_type": "practice",
                        "suggested_duration_minutes": 30,
                        "difficulty": "medium",
                        "cognitive_load": "high",
                        "notes": "Continue with more varied problem types"
                    },
                    {
                        "title": "Deep practice: Advanced problems - Part 1",
                        "task_type": "deep_practice",
                        "suggested_duration_minutes": 30,
                        "difficulty": "high",
                        "cognitive_load": "high",
                        "notes": "Challenge yourself with complex scenarios"
                    },
                    {
                        "title": "Deep practice: Advanced problems - Part 2",
                        "task_type": "deep_practice",
                        "suggested_duration_minutes": 30,
                        "difficulty": "high",
                        "cognitive_load": "high",
                        "notes": "Master difficult problem-solving techniques"
                    },
                    {
                        "title": "Practice: Application and integration",
                        "task_type": "practice",
                        "suggested_duration_minutes": 30,
                        "difficulty": "medium",
                        "cognitive_load": "high",
                        "notes": "Combine multiple concepts in problem-solving"
                    },
                    {
                        "title": "Revision: Review all concepts",
                        "task_type": "revision",
                        "suggested_duration_minutes": 30,
                        "difficulty": "low",
                        "cognitive_load": "low",
                        "notes": "Go through notes and identify weak areas"
                    },
                    {
                        "title": "Revision: Practice weak areas",
                        "task_type": "revision",
                        "suggested_duration_minutes": 30,
                        "difficulty": "medium",
                        "cognitive_load": "medium",
                        "notes": "Focus on topics you find challenging"
                    },
                    {
                        "title": "Mock test: Timed practice",
                        "task_type": "mock_test",
                        "suggested_duration_minutes": 45,
                        "difficulty": "high",
                        "cognitive_load": "high",
                        "notes": "Simulate exam conditions with time pressure"
                    },
                    {
                        "title": "Final review and relaxation",
                        "task_type": "revision",
                        "suggested_duration_minutes": 25,
                        "difficulty": "low",
                        "cognitive_load": "low",
                        "notes": "Light review, mental preparation, stay confident"
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

    # ==================== Phase 3: Diagnostic Analysis ====================

    def analyze_diagnostic_test(
        self,
        diagnostic_test_id: int,
        event_title: str,
        questions_data: List[Dict[str, Any]]
    ) -> Optional[DiagnosticAnalysisResult]:
        """
        Analyze a diagnostic test to identify error patterns and learning gaps.

        This implements AI Use Case #4: Diagnostic Test Analysis

        Args:
            diagnostic_test_id: ID of the diagnostic test
            event_title: Title of the related event
            questions_data: List of question dicts with:
                - question_number
                - question_text
                - correct_answer
                - user_answer
                - topic
                - is_correct

        Returns:
            DiagnosticAnalysisResult dict or None if AI fails
        """
        try:
            # Load prompt template
            prompt_template = self._load_prompt_template('diagnostic_analysis.txt')

            # Format questions for the prompt
            questions_formatted = []
            for q in questions_data:
                questions_formatted.append(
                    f"{q['question_number']}. \"{q['question_text']}\" - "
                    f"Correct: \"{q['correct_answer']}\" - "
                    f"User: \"{q['user_answer']}\" - "
                    f"Topic: \"{q.get('topic', 'Uncategorized')}\" - "
                    f"{'Correct' if q['is_correct'] else 'Incorrect'}"
                )

            # Construct full prompt
            prompt = f"{prompt_template}\n\n## DIAGNOSTIC TEST TO ANALYZE\n\n"
            prompt += f"Event: {event_title}\n\n"
            prompt += "Questions:\n" + "\n".join(questions_formatted)
            prompt += "\n\nProvide your analysis in JSON format:"

            logger.info(f"Analyzing diagnostic test {diagnostic_test_id} with {len(questions_data)} questions")

            # Call AI
            response = self._call_ai_provider(prompt)
            analysis = self._parse_json_response(response)

            # Validate schema
            validate_diagnostic_analysis(analysis)

            logger.info(
                f"Diagnostic analysis complete: {analysis['score_percentage']}% score, "
                f"{len(analysis['error_groups'])} error groups"
            )

            return analysis

        except Exception as e:
            logger.error(f"Diagnostic analysis failed: {str(e)}", exc_info=True)
            # Return basic analysis as fallback
            return self._fallback_diagnostic_analysis(questions_data)

    def _fallback_diagnostic_analysis(self, questions_data: List[Dict]) -> DiagnosticAnalysisResult:
        """Fallback analysis if AI fails."""
        total = len(questions_data)
        correct = sum(1 for q in questions_data if q['is_correct'])
        incorrect = total - correct

        # Group errors by topic
        error_groups = {}
        for q in questions_data:
            if not q['is_correct']:
                topic = q.get('topic', 'Uncategorized')
                if topic not in error_groups:
                    error_groups[topic] = {
                        'topic': topic,
                        'error_count': 0,
                        'question_numbers': [],
                        'error_types': [],
                        'severity': 'medium'
                    }
                error_groups[topic]['error_count'] += 1
                error_groups[topic]['question_numbers'].append(q['question_number'])

        error_groups_list = list(error_groups.values())
        dominant_topic = max(error_groups_list, key=lambda x: x['error_count'])['topic'] if error_groups_list else None

        return {
            'total_questions': total,
            'correct_count': correct,
            'incorrect_count': incorrect,
            'score_percentage': int((correct / total) * 100) if total > 0 else 0,
            'error_groups': error_groups_list,
            'dominant_error_topic': dominant_topic,
            'recommended_review_topics': [g['topic'] for g in error_groups_list[:3]],
            'analysis_summary': f"Basic analysis: {correct}/{total} correct ({int((correct/total)*100)}% score). "
                              f"AI analysis unavailable, showing basic error grouping."
        }

    # ==================== Phase 3: Plan Adjustment ====================

    def suggest_plan_adjustments(
        self,
        event_title: str,
        event_date: datetime,
        emotional_state: Optional[Dict[str, str]],
        diagnostic_results: Optional[Dict[str, Any]],
        current_sessions: List[Dict[str, Any]]
    ) -> Optional[PlanAdjustmentResult]:
        """
        Suggest adjustments to study plan based on emotional state and diagnostic results.

        This implements AI Use Case #5: Plan Adjustment Suggestions

        Args:
            event_title: Title of the event
            event_date: When the event occurs
            emotional_state: Dict with energy/stress/focus levels (or None)
            diagnostic_results: Recent diagnostic test results (or None)
            current_sessions: List of existing study sessions with titles and durations

        Returns:
            PlanAdjustmentResult dict or None if no adjustments needed
        """
        try:
            # Determine trigger
            triggers = []
            if emotional_state:
                if emotional_state.get('stress') == 'high':
                    triggers.append('high_stress')
                if emotional_state.get('energy') == 'low':
                    triggers.append('low_energy')
                if emotional_state.get('focus') == 'low':
                    triggers.append('low_focus')

            if diagnostic_results:
                score = diagnostic_results.get('score_percentage', 100)
                if score < 60:
                    triggers.append('low_diagnostic_score')

            if not triggers:
                logger.info("No triggers for plan adjustment")
                return None

            triggered_by = '_and_'.join(triggers)

            # Load prompt template
            prompt_template = self._load_prompt_template('plan_adjustment.txt')

            # Construct full prompt
            prompt = f"{prompt_template}\n\n## STUDENT SITUATION\n\n"
            prompt += f"### Event\n"
            prompt += f"- Title: {event_title}\n"
            prompt += f"- Date: {event_date.strftime('%Y-%m-%d')}\n\n"

            if emotional_state:
                prompt += f"### Emotional State\n"
                prompt += f"- Energy: {emotional_state.get('energy', 'unknown')}\n"
                prompt += f"- Stress: {emotional_state.get('stress', 'unknown')}\n"
                prompt += f"- Focus: {emotional_state.get('focus', 'unknown')}\n\n"

            if diagnostic_results:
                prompt += f"### Diagnostic Results\n"
                prompt += f"- Score: {diagnostic_results.get('score_percentage', 0)}%\n"
                prompt += f"- Dominant error topic: {diagnostic_results.get('dominant_error_topic', 'None')}\n\n"

            prompt += f"### Current Study Sessions\n"
            for session in current_sessions:
                prompt += f"- \"{session['title']}\" ({session['duration_minutes']} minutes)\n"

            prompt += "\n\nProvide your plan adjustment suggestion in JSON format:"

            logger.info(f"Requesting plan adjustments for {event_title}, triggered by: {triggered_by}")

            # Call AI
            response = self._call_ai_provider(prompt)
            adjustment = self._parse_json_response(response)

            # Validate schema
            validate_plan_adjustment(adjustment)

            logger.info(
                f"Plan adjustment suggested: {len(adjustment['adjustments'])} changes"
            )

            return adjustment

        except Exception as e:
            logger.error(f"Plan adjustment suggestion failed: {str(e)}", exc_info=True)
            return None


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
