# Troubleshooting Guide - UI Not Showing AI Tasks

If you're not seeing AI-generated tasks in the UI after creating an event, follow these steps:

---

## Quick Fix (Most Common Issue)

### The server needs to be restarted after code changes!

```bash
# 1. Stop the server (if running)
# Press Ctrl+C in the terminal where server is running

# 2. Start the server again
python manage.py runserver

# 3. Hard refresh your browser
# Windows/Linux: Ctrl+Shift+R
# Mac: Cmd+Shift+R
```

---

## Step-by-Step Verification

### Step 1: Verify Code Changes Are in Place

Check that these files have been updated:

1. **events/views.py** - Line 9 should have:
   ```python
   from ai.event_integration import generate_ai_study_sessions
   ```

2. **events/views.py** - `generate_study_sessions()` function (around line 85) should call AI:
   ```python
   ai_sessions = generate_ai_study_sessions(event, force_regenerate=True)
   ```

3. **templates/events/event_detail.html** - Should have "Start with Timer" button (around line 95):
   ```html
   <button type="submit" class="btn btn-sm btn-success w-100">
       <i class="bi bi-stopwatch"></i> Start with Timer
   </button>
   ```

### Step 2: Restart Django Server

**IMPORTANT:** Django doesn't auto-reload Python code in all cases. Always restart:

```bash
# Stop server
Ctrl+C

# Start server
python manage.py runserver
```

### Step 3: Clear Browser Cache

Old pages might be cached. Try:

**Option A: Hard Refresh**
- Windows/Linux: `Ctrl+Shift+R`
- Mac: `Cmd+Shift+R`

**Option B: Incognito/Private Window**
- Open a new incognito/private window
- Navigate to your site

**Option C: Clear Cache**
- Browser Settings → Clear Browsing Data
- Select "Cached images and files"
- Clear

### Step 4: Delete Old Test Data

Old events created before the fix won't have AI tasks. Delete them:

```bash
# Using Django shell
python manage.py shell
```

Then in the shell:
```python
from events.models import Event
# Delete all events (if testing)
Event.objects.all().delete()

# Or delete specific event
Event.objects.filter(id=YOUR_EVENT_ID).delete()
```

### Step 5: Create a Fresh Event

1. Go to http://127.0.0.1:8000/users/login/
2. Login with your account
3. Click "Events" → "Create New Event"
4. Fill in details:
   - **Title:** "Test - Python Exam"
   - **Type:** Exam
   - **Date:** 7 days from now
   - **Subject:** Computer Science
   - **Priority:** High
   - **Prep Time:** 6 (hours)
   - **Description:** "OOP, data structures, algorithms"
5. Click "Create Event"

### Step 6: Verify AI Tasks Appear

After creating the event, you should see:

✅ **Redirected to event detail page**
✅ **4 study sessions visible**
✅ **Each session has detailed content like:**
```
Task 1/4: Review key concepts and fundamentals

Type: Concept Review
Difficulty: Low
Duration: 30 minutes

Tips:
Start with understanding core principles
```
✅ **"Start with Timer" button visible on each pending task**

---

## Common Issues & Solutions

### Issue 1: "No study sessions yet"

**Symptoms:** Event detail page shows "No study sessions yet"

**Causes:**
- Server not restarted after code changes
- AI import error
- Event created before code fix

**Solutions:**
1. Restart server (Ctrl+C, then `python manage.py runserver`)
2. Check server console for errors
3. Delete the event and create a new one

---

### Issue 2: Sessions show but content is generic

**Symptoms:** Sessions appear but say "Study session 1 of 4" (no AI content)

**Causes:**
- AI is falling back to deterministic mode
- AI service not initialized

**Solutions:**
1. Check AI settings in `settings.py`:
   ```python
   AI_ENABLED = True
   AI_PROVIDER = 'mock'
   ```

2. Test AI directly:
   ```bash
   python test_ai_simple.py
   ```

3. Check server logs for AI errors

---

### Issue 3: "Start with Timer" button missing

**Symptoms:** Only see "Start" and "Skip" buttons, no timer button

**Causes:**
- Template not updated
- Browser cache
- Server not restarted

**Solutions:**
1. Verify template file was updated
2. Restart server
3. Hard refresh browser (Ctrl+Shift+R)
4. Try incognito window

---

### Issue 4: Server errors when creating event

**Symptoms:** Error page or 500 error when creating event

**Causes:**
- Missing migrations
- Import errors
- Database issues

**Solutions:**
1. Check for migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Check server console for error messages

3. Verify imports work:
   ```bash
   python manage.py shell
   ```
   ```python
   from ai.event_integration import generate_ai_study_sessions
   from events.views import generate_study_sessions
   # Should not error
   ```

---

## Verification Checklist

Run through this checklist:

- [ ] Code changes are in place (check files manually)
- [ ] Django server was restarted after code changes
- [ ] Browser cache cleared (hard refresh or incognito)
- [ ] Old test events deleted
- [ ] Created a NEW event after code changes
- [ ] AI settings enabled in settings.py
- [ ] No errors in server console
- [ ] Can import AI modules in Django shell

---

## Test AI is Working

Run these commands to verify AI:

```bash
# Test 1: Basic AI
python test_ai_simple.py
# Should show: [OK] All critical AI functions are working!

# Test 2: Event integration
python verify_ai_working.py
# Should show: [PASS] AI integrates with Event/StudySession models

# Test 3: Event creation
python test_event_creation.py
# Should show: [OK] Generated 4 study sessions with AI content
```

---

## Manual Database Check

If you want to see what's actually in the database:

```bash
python manage.py shell
```

```python
from events.models import Event
from study_sessions.models import StudySession

# Get latest event
event = Event.objects.latest('created_at')
print(f"Event: {event.title}")

# Get its sessions
sessions = event.study_sessions.all()
print(f"Sessions: {sessions.count()}")

# Check first session content
if sessions.count() > 0:
    first = sessions.first()
    print(f"Content: {first.suggested_content}")

    # Is it AI?
    if "Task" in first.suggested_content:
        print("AI-generated: YES")
    else:
        print("AI-generated: NO (deterministic)")
```

---

## Still Not Working?

### Option 1: Fresh Start

```bash
# 1. Stop server
Ctrl+C

# 2. Delete test database (if testing)
rm db.sqlite3  # or delete file manually

# 3. Recreate database
python manage.py migrate
python manage.py populate_focus_models
python manage.py createsuperuser

# 4. Start server
python manage.py runserver

# 5. Create new event via web UI
```

### Option 2: Check Server Logs

Look for errors in the terminal where server is running:
- Import errors
- AI service errors
- Template errors
- Database errors

### Option 3: Enable Debug Mode

In `settings.py`, ensure:
```python
DEBUG = True
```

This will show detailed error pages.

---

## Expected Behavior (After Fix)

### When You Create an Event:

1. Fill form and click "Create Event"
2. Redirected to event detail page
3. See message: "Event created successfully with auto-generated study sessions!"
4. See 4-7 study sessions listed
5. Each session has:
   - Date and time
   - Duration (25-60 minutes)
   - Detailed AI-generated content with:
     - Task number (1/4, 2/4, etc.)
     - Task title
     - Type (Concept Review, Practice, etc.)
     - Difficulty (Low, Medium, High)
     - Duration in minutes
     - Tips section
6. "Start with Timer" button on each pending session

### When You Click "Start with Timer":

1. Redirected to Focus Timer page
2. Timer starts automatically
3. See message: "Focus session started for [Event Name]!"
4. Timer shows countdown
5. After timer ends:
   - Session marked "completed"
   - Break recommendation shown
   - Event progress updated

---

## Contact Points

If still having issues, check:

1. **Server Console** - Look for Python errors
2. **Browser Console** (F12) - Look for JavaScript errors
3. **Network Tab** (F12) - Check if requests failing
4. **Test Scripts** - Run diagnostic scripts above

---

## Summary: Most Common Fix

**90% of "UI not updating" issues are solved by:**

```bash
# 1. Restart server
Ctrl+C
python manage.py runserver

# 2. Hard refresh browser
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (Mac)

# 3. Create NEW event (old ones won't have AI)
```

---

**Last Updated:** January 16, 2026
