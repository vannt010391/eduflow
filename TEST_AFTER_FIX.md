# Test After Import Error Fix ✅

**Import Error Fixed!** ✅

The error was:
```
ImportError: cannot import name 'LANGUAGE_SESSION_KEY' from 'django.utils.translation'
```

**Fixed by:** Defining `LANGUAGE_SESSION_KEY = '_language'` directly in the middleware file.

---

## 🚀 Test NOW

### Step 1: Start Server
```bash
python manage.py runserver
```

**Should start without errors now!** ✅

### Step 2: Clear Browser Data
```
Ctrl+Shift+Delete (clear cache and cookies)
OR
Ctrl+Shift+N (incognito mode)
```

### Step 3: Open Application
```
F12 (open console)
http://localhost:8000
```

### Step 4: Check Default State

**You should see:**
- Badge: `[en]`
- Text: "Dashboard", "Events", "Today's Tasks"
- Console: `Language cookie: django_language=en` (or `undefined`)

**If you see Vietnamese instead:**
→ Old session still active
→ Close browser completely and reopen
→ Or run: `python manage.py shell -c "from django.contrib.sessions.models import Session; Session.objects.all().delete()"`

### Step 5: Test English → Vietnamese

1. Click language dropdown
2. Click "Tiếng Việt"
3. Watch page reload

**Expected:**
- Badge changes: `[en]` → `[vi]`
- Text changes: "Dashboard" → "Bảng điều khiển"
- URL gets `?nocache=...` parameter

### Step 6: Test Vietnamese → English

1. Click language dropdown
2. Click "English"
3. Watch page reload

**Expected:**
- Badge changes: `[vi]` → `[en]`
- Text changes: "Bảng điều khiển" → "Dashboard"
- URL gets `?nocache=...` parameter

### Step 7: Verify Cookie Matches UI

**Open DevTools:**
```
F12 → Application tab → Cookies → localhost:8000
```

**Find `django_language` cookie:**

**When in English mode:**
- Cookie value: `en`
- Badge: `[en]`
- Text: English ✅

**When in Vietnamese mode:**
- Cookie value: `vi`
- Badge: `[vi]`
- Text: Vietnamese ✅

**Cookie and UI should ALWAYS match now!**

---

## ✅ Success Checklist

- [ ] Server starts without errors
- [ ] Default is English `[en]`
- [ ] Can switch to Vietnamese
- [ ] Badge changes to `[vi]`
- [ ] Text changes to Vietnamese
- [ ] Can switch back to English
- [ ] Badge changes to `[en]`
- [ ] Text changes to English
- [ ] Cookie value matches badge
- [ ] No console errors

**If ALL pass:** 🎉 **WORKING PERFECTLY!**

---

## 🔍 If Still Not Working

**Check 1: Server Running?**
```bash
python manage.py runserver
```
Should show no errors.

**Check 2: Middleware Loading?**
Check server console for any middleware errors.

**Check 3: Cookie vs Badge**
- Open DevTools → Application → Cookies
- Check if `django_language` value matches badge `[en]` or `[vi]`

**If cookie = `en` but badge = `[vi]`:**
→ Middleware not clearing session
→ Send me screenshot of console and cookies

**Check 4: Sessions**
Run:
```bash
python manage.py shell -c "from django.contrib.sessions.models import Session; print('Sessions:', Session.objects.count())"
```

If count > 0, clear them:
```bash
python manage.py shell -c "from django.contrib.sessions.models import Session; Session.objects.all().delete(); print('Cleared')"
```

---

## 📝 What Was Fixed

**File:** `eduflow_ai/middleware.py`

**Before (broken):**
```python
from django.utils.translation import LANGUAGE_SESSION_KEY  # ❌ Wrong import
```

**After (fixed):**
```python
from django.conf import settings

# Define it ourselves
LANGUAGE_SESSION_KEY = '_language'  # ✅ Correct!
```

Django's `LocaleMiddleware` uses `'_language'` as the session key internally, so we define it ourselves.

---

## 🎯 Quick Summary

1. ✅ Import error fixed
2. ✅ Server should start now
3. ✅ Middleware will clear session language
4. ✅ Django will use cookie only
5. ✅ Cookie and UI will match

**Test it now!** Start the server and try switching languages! 🚀
