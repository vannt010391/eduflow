# Requirements Installation Guide

This guide explains the different requirement files and how to install dependencies for EduFlow AI.

---

## 📁 Requirement Files

### 1. `requirements.txt` (Minimal - Recommended for Testing)
Contains only the essential dependencies needed to run EduFlow AI with **mock AI provider**.

**Includes:**
- Django 4.2.7
- django-crispy-forms
- crispy-bootstrap4

**Use this when:**
- Testing the application
- You don't want to use real AI yet
- You want minimal dependencies

**Install:**
```bash
pip install -r requirements.txt
```

---

### 2. `requirements-full.txt` (Complete)
Contains all possible dependencies including optional AI providers, development tools, and production packages.

**Includes:**
- All core dependencies
- AI providers (OpenAI, Anthropic) - commented out
- Development tools (pytest, black, flake8) - commented out
- Production tools (gunicorn, whitenoise) - commented out

**Use this when:**
- You want to see all available options
- Setting up a development environment
- Preparing for production deployment

**Install:**
```bash
pip install -r requirements-full.txt
```

---

## 🤖 AI Provider Installation

The AI functionality works with **3 providers**:

### Option 1: Mock Provider (Default) ✅ RECOMMENDED FOR TESTING
**Cost:** FREE
**Setup:** None needed - already configured

```python
# In settings.py (already configured)
AI_ENABLED = True
AI_PROVIDER = 'mock'
AI_API_KEY = None
```

**Features:**
- Generates realistic test data
- No API costs
- Perfect for development and testing
- All AI features work

---

### Option 2: OpenAI (GPT-4, GPT-3.5-turbo)
**Cost:** ~$0.003 per event (~1 cent for 3-4 events)
**Best for:** Production use, high quality

**Installation:**
```bash
pip install openai
```

**Configuration:**
1. Get API key from https://platform.openai.com/api-keys
2. Update `settings.py`:
```python
AI_ENABLED = True
AI_PROVIDER = 'openai'
AI_API_KEY = 'sk-...'  # Your OpenAI API key
AI_MODEL = 'gpt-3.5-turbo'  # Or 'gpt-4'
```

**Recommended Model:**
- **gpt-3.5-turbo**: Cost-effective, fast, good quality
- **gpt-4**: Higher quality, more expensive

---

### Option 3: Anthropic (Claude)
**Cost:** Similar to OpenAI
**Best for:** Alternative to OpenAI, different AI style

**Installation:**
```bash
pip install anthropic
```

**Configuration:**
1. Get API key from https://console.anthropic.com/
2. Update `settings.py`:
```python
AI_ENABLED = True
AI_PROVIDER = 'anthropic'
AI_API_KEY = 'sk-ant-...'  # Your Anthropic API key
AI_MODEL = 'claude-3-haiku-20240307'  # Or other Claude models
```

**Recommended Model:**
- **claude-3-haiku**: Fast and affordable
- **claude-3-sonnet**: Balanced performance
- **claude-3-opus**: Highest quality

---

## 📦 Installation Steps

### Basic Installation (Mock AI)

```bash
# 1. Create virtual environment (optional but recommended)
python -m venv venv

# 2. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install core requirements
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create focus models
python manage.py populate_focus_models

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

### With Real AI Provider

```bash
# 1-6. Same as above

# 7. Install AI provider
pip install openai  # or anthropic

# 8. Update settings.py with your API key
# (See configuration above)

# 9. Run server
python manage.py runserver
```

---

## 🧪 Testing AI Installation

### Test 1: Basic AI Test
```bash
python test_ai_simple.py
```

**Expected output:**
```
[OK] Django setup successful
[OK] All AI modules imported successfully
[OK] AI is enabled with mock provider
[OK] AI Service initialized
[OK] Learning plan generated successfully
[OK] Plan validation passed
```

### Test 2: Event Integration Test
```bash
python verify_ai_working.py
```

**Expected output:**
```
[PASS] AI service is initialized and working
[PASS] AI can generate learning plans
[PASS] AI integrates with Event/StudySession models
[PASS] Generated sessions have proper structure
```

---

## 🔍 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'openai'"
**Solution:** Install OpenAI package
```bash
pip install openai
```

### Issue: "AI plan generation failed"
**Check:**
1. AI_ENABLED = True in settings.py
2. AI_PROVIDER is set correctly
3. If using OpenAI/Anthropic, API key is set

### Issue: "Invalid API key"
**Check:**
1. API key is correct and not expired
2. API key has proper permissions
3. You have credits/billing set up with the provider

---

## 💰 Cost Estimates

### Mock Provider
- **Cost per event:** $0 (FREE)
- **Monthly cost (unlimited):** $0

### OpenAI (gpt-3.5-turbo)
- **Cost per event:** ~$0.003 (less than 1 cent)
- **100 users, 5 events/month:** ~$1.50/month
- **1,000 users, 5 events/month:** ~$15/month

### OpenAI (gpt-4)
- **Cost per event:** ~$0.03 (3 cents)
- **100 users, 5 events/month:** ~$15/month
- **1,000 users, 5 events/month:** ~$150/month

### Anthropic (claude-3-haiku)
- **Cost per event:** ~$0.002-0.005
- Similar to GPT-3.5-turbo

**Note:** Costs include 24-hour caching which reduces actual costs by 50-70%

---

## 📚 Additional Information

### Dependencies Explanation

| Package | Purpose | Required? |
|---------|---------|-----------|
| Django | Web framework | Yes |
| django-crispy-forms | Form styling | Yes |
| crispy-bootstrap4 | Bootstrap 4 support | Yes |
| openai | OpenAI API client | Optional (for real AI) |
| anthropic | Anthropic API client | Optional (for real AI) |

### Python Version
- **Required:** Python 3.8 or higher
- **Tested:** Python 3.10, 3.11
- **Recommended:** Python 3.10+

### Database
- **Default:** SQLite (built into Python)
- **Production:** PostgreSQL (requires psycopg2-binary)
- **Alternative:** MySQL (requires mysqlclient)

---

## 🚀 Next Steps

After installing requirements:

1. ✅ Run tests to verify installation
2. ✅ Create a superuser account
3. ✅ Start the development server
4. ✅ Create a test event to see AI in action
5. 📝 Read [AI_VERIFICATION_REPORT.md](AI_VERIFICATION_REPORT.md) for details

---

## 📞 Support

If you encounter issues:
1. Check [README.md](README.md) troubleshooting section
2. Review [AI_IMPLEMENTATION_GUIDE.md](AI_IMPLEMENTATION_GUIDE.md)
3. Check Django logs for errors
4. Verify all settings in `settings.py`

---

**Last Updated:** January 16, 2026
**Django Version:** 4.2.7
**Python Version:** 3.8+
