# EduFlow AI - Quick Start Guide

Get EduFlow AI up and running in 5 minutes!

---

## 🚀 Installation (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py migrate
python manage.py populate_focus_models
python manage.py createsuperuser
```

### Step 3: Run Server
```bash
python manage.py runserver
```

**Done!** Visit http://127.0.0.1:8000

---

## 🎯 What You Get

### ✅ Working Features
- Event management (exams, assignments, quizzes)
- Auto-generated study sessions
- Focus timer (Pomodoro, Extended, Deep Work)
- Analytics dashboard
- **AI-powered learning plans** (using mock provider)
- Multilingual support (English/Vietnamese)

### 🤖 AI Status
- **Current:** Mock AI provider (FREE, no API key needed)
- **Generates:** Realistic study plans with 4-7 tasks per event
- **Quality:** Production-ready test data

---

## 📝 Create Your First Event

1. Login at http://127.0.0.1:8000/users/login/
2. Go to "Events" → "Create New Event"
3. Fill in:
   - Title: "Python Midterm Exam"
   - Type: Exam
   - Date: 7 days from now
   - Prep time: 6 hours
   - Subject: Computer Science
4. Click "Create Event"

**Result:** AI automatically generates 4 study sessions!

---

## 🔬 Test AI Functionality

```bash
# Test 1: Basic AI
python test_ai_simple.py

# Test 2: Event Integration
python verify_ai_working.py
```

**Expected:** All tests pass with [OK] status

---

## ⚡ Upgrade to Real AI (Optional)

### For OpenAI (GPT-4/3.5):
```bash
# 1. Install
pip install openai

# 2. Get API key from https://platform.openai.com/

# 3. Edit settings.py:
AI_PROVIDER = 'openai'
AI_API_KEY = 'sk-your-key-here'
AI_MODEL = 'gpt-3.5-turbo'

# 4. Restart server
```

**Cost:** ~$0.003 per event (less than 1 cent)

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [REQUIREMENTS_GUIDE.md](REQUIREMENTS_GUIDE.md) | Installation details |
| [AI_VERIFICATION_REPORT.md](AI_VERIFICATION_REPORT.md) | AI test results |
| [AI_IMPLEMENTATION_GUIDE.md](AI_IMPLEMENTATION_GUIDE.md) | AI technical guide |

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
```bash
pip install -r requirements.txt
```

### "No such table" error
```bash
python manage.py migrate
```

### "No FocusModel objects"
```bash
python manage.py populate_focus_models
```

### AI not generating plans
- Check: AI_ENABLED = True in settings.py
- Check: AI_PROVIDER = 'mock' in settings.py
- Run: `python test_ai_simple.py` to diagnose

---

## 🎓 Key URLs

| URL | Description |
|-----|-------------|
| / | Dashboard (auto-redirects) |
| /users/login/ | Login page |
| /users/register/ | Register new account |
| /events/ | Event list |
| /events/create/ | Create new event |
| /sessions/today/ | Today's study sessions |
| /focus/timer/ | Focus timer |
| /analytics/ | Analytics dashboard |
| /admin/ | Django admin |

---

## 💡 Tips

1. **Start with mock AI** - It's free and works great for testing
2. **Create test events** - Try different event types to see AI variations
3. **Check analytics** - View your study patterns
4. **Customize focus models** - Choose Pomodoro, Extended, or Deep Work
5. **Use multilingual** - Switch between English and Vietnamese

---

## 🎉 You're Ready!

EduFlow AI is now running with:
- ✅ Full event management
- ✅ AI-powered study planning
- ✅ Focus timer & breaks
- ✅ Analytics tracking
- ✅ Zero API costs (mock AI)

**Next:** Create events and watch AI generate your study plan!

---

**Need Help?** See [REQUIREMENTS_GUIDE.md](REQUIREMENTS_GUIDE.md) for detailed instructions.
