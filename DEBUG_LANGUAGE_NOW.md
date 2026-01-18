# Debug Language Switching - IMMEDIATE TEST

## 🎯 Quick Test (30 seconds)

### Step 1: Start Server
```bash
python manage.py runserver
```

### Step 2: Open Test Page
Go to: **http://localhost:8000/test-lang/**

### Step 3: What You'll See
A test page showing:
- **Active Language:** vi or en
- **Cookie Value:** django_language value
- Two buttons to switch languages

### Step 4: Click Buttons
1. Click "Switch to English (en)" button
2. Page should reload
3. Check if "Active Language" changed from `vi` to `en`

4. Click "Switch to Vietnamese (vi)" button
5. Page should reload
6. Check if "Active Language" changed from `en` to `vi`

## ✅ Success Criteria

**WORKING:** If "Active Language" changes when you click the buttons
**NOT WORKING:** If "Active Language" stays the same

## 📸 Take Screenshot

Please take screenshots of:
1. **BEFORE clicking** - showing "Active Language: vi"
2. **AFTER clicking "Switch to English"** - should show "Active Language: en"
3. **Browser Console** (F12) - any errors?
4. **Network Tab** (F12) - POST to /i18n/setlang/ status code

## 🐛 If It Doesn't Work

Look at the test page - it shows:
- Current active language
- Cookie value
- All cookies
- Session info

**Send me this info!**

## 🔧 This Test Bypasses

This test page:
- ✅ Has CSRF token properly included
- ✅ Uses simple forms
- ✅ Shows exact state
- ✅ Redirects back to same page

If this works but the main site doesn't:
→ Problem is in base.html forms

If this doesn't work:
→ Problem is deeper (middleware/settings)

## ⚡ Super Quick Check

Just open: **http://localhost:8000/test-lang/**

And click the buttons!

You'll immediately see if language switching works or not.

---

**This test page will tell us EXACTLY what's wrong!** 🎯
