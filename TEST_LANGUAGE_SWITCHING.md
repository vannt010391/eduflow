# Test Language Switching - Simple Instructions

**Date:** 2026-01-16

---

## 🎯 Quick Test (2 minutes)

### Step 1: Start Server
```bash
python manage.py runserver
```

### Step 2: Open Browser
1. Go to: `http://localhost:8000`
2. Login if needed

### Step 3: Look at Navigation Bar
You should see the language dropdown with a **badge** showing the language code:

```
🌐 Tiếng Việt [vi]
```
or
```
🌐 English [en]
```

### Step 4: Switch Language
1. Click on the language dropdown
2. Click the OTHER language (not the one with checkmark)
3. **Watch the badge** - it should change from `vi` to `en` or vice versa

---

## ✅ If Badge Changes

**CONGRATULATIONS!** Language switching IS working!

The reason you might not see text changes is because translation files need to be compiled.

To get full translations:
1. Install gettext tools (see below)
2. Run: `python manage.py compilemessages`
3. Restart server

---

## ❌ If Badge Doesn't Change

Open browser DevTools (press F12) and check:

### Console Tab
Look for these messages:
```
Current URL: http://localhost:8000/dashboard/
Language cookie: django_language=vi
Language form submitted
Action: /i18n/setlang/
Language: en
Next: /dashboard/
```

### Network Tab
1. Click language switch
2. Look for POST request to `/i18n/setlang/`
3. Should see Status: 302 (redirect)

### Application Tab → Cookies
Look for cookie named `django_language`
- Value should be `vi` or `en`
- Should change when you click language switch

**Send me screenshots of these tabs if it's not working!**

---

## 📦 Install gettext Tools (Optional - For Full Translations)

### Windows:
**Option 1: Chocolatey (Recommended)**
```bash
choco install gettext
```

**Option 2: Manual Download**
1. Visit: https://mlocati.github.io/articles/gettext-iconv-windows.html
2. Download the installer
3. Run installer
4. Add to PATH

**Option 3: MSYS2**
```bash
# If you have MSYS2 installed:
pacman -S gettext
```

### After Installing gettext:
```bash
# Compile translations
python manage.py compilemessages

# Restart server
python manage.py runserver
```

---

## 🔍 What Each Component Does

### The Badge `[vi]` or `[en]`
- Shows the **actual current language code**
- Changes immediately when language switches
- Confirms switching mechanism works

### The Language Name "Tiếng Việt" or "English"
- Shows user-friendly language name
- Should match the badge code

### The Checkmark ✓
- Shows which language is currently active
- Should be on the same language as the badge

---

## 📸 What You Should See

### Before Clicking (in Vietnamese):
```
Navbar: 🌐 Tiếng Việt [vi] ▼
Dropdown:
  ✓ Tiếng Việt    ← has checkmark
    English
```

### After Clicking "English":
```
Navbar: 🌐 English [en] ▼
Dropdown:
    Tiếng Việt
  ✓ English        ← checkmark moved
```

**The badge [vi] → [en] is the KEY indicator!**

---

## 🚨 Emergency Debug

If nothing works, add this to see what's happening:

1. Open `templates/base.html`
2. Find the language dropdown section (around line 97)
3. Add this RIGHT AFTER line 107:

```html
<!-- EMERGENCY DEBUG -->
<li class="nav-item">
    <span class="nav-link text-warning">
        DEBUG: {{ CURRENT_LANG }} | Cookie: {{ request.COOKIES.django_language }}
    </span>
</li>
```

This will show BOTH the detected language AND the cookie value.

---

## 📝 Report Format

If it still doesn't work, please report:

**1. What badge shows:**
- [ ] Shows [vi]
- [ ] Shows [en]
- [ ] Shows nothing
- [ ] Doesn't change when clicking

**2. Browser console output:**
```
[Paste console messages here]
```

**3. Network tab for /i18n/setlang/:**
- Status Code: ___
- Response Headers: ___

**4. Cookie value:**
- django_language = ___

**5. Browser:**
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Other: ___

---

## ✨ Expected Final Result

Once everything works + translations compiled:

### Vietnamese (default):
- Badge: [vi]
- Dropdown: 🌐 Tiếng Việt
- Navigation: Bảng điều khiển, Sự kiện, Nhiệm vụ, etc.

### English:
- Badge: [en]
- Dropdown: 🌐 English
- Navigation: Dashboard, Events, Tasks, etc.

### Switching:
- Instant reload
- All text changes
- Cookie persists forever (well, 1 year)

---

**The badge is your friend! Watch it carefully!** 🎯
