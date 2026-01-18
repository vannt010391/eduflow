# Language Switching Troubleshooting Guide

**Issue:** Can't switch from English to Vietnamese
**Date:** 2026-01-16

---

## 🔍 Diagnostic Steps

### Step 1: Check Browser Console
1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Reload the page
4. You should see logs like:
   ```
   Current URL: http://localhost:8000/dashboard/
   Language cookie: django_language=vi
   ```

### Step 2: Test Language Switch
1. Click the language dropdown
2. Click "Tiếng Việt" or "English"
3. Watch Console for:
   ```
   Language form submitted
   Action: /i18n/setlang/
   Language: vi (or en)
   Next: /dashboard/
   ```

### Step 3: Check Network Tab
1. Open Network tab in DevTools
2. Click language switch
3. Look for POST request to `/i18n/setlang/`
4. Check:
   - **Status Code:** Should be 302 (Redirect)
   - **Form Data:** Should have `language=vi` and `next=/dashboard/`
   - **Response Headers:** Should have `Set-Cookie: django_language=vi`

### Step 4: Check Cookies
1. Go to Application tab → Cookies
2. Look for cookie named `django_language`
3. Check:
   - **Value:** Should be `vi` or `en`
   - **Path:** Should be `/`
   - **Expires:** Should be ~1 year from now

---

## 🐛 Common Issues & Fixes

### Issue 1: Cookie Not Being Set

**Symptoms:**
- Language switches but doesn't persist
- Cookie not visible in Application tab

**Possible Causes:**
1. **Browser blocks third-party cookies**
   - Solution: Check browser settings, allow cookies for localhost

2. **CSRF token missing**
   - Solution: Check form has `{% csrf_token %}`
   - Verify token in Network tab POST data

3. **Cookie settings incorrect**
   - Solution: Check settings.py has all cookie settings

**Fix:**
```bash
# Clear all cookies
# In browser: Settings → Privacy → Clear browsing data → Cookies

# Then restart server
python manage.py runserver
```

### Issue 2: Page Doesn't Reload

**Symptoms:**
- Click language, nothing happens
- No network request in DevTools

**Possible Causes:**
1. **JavaScript error preventing form submission**
   - Check Console for errors

2. **Form not submitting**
   - Check form has correct action URL

**Fix:**
Add this temporary debug to base.html before the closing `</body>` tag:
```html
<script>
document.querySelectorAll('.language-form button').forEach(btn => {
    btn.addEventListener('click', function(e) {
        console.log('Button clicked!', this.parentForm);
        alert('Switching language to: ' + this.parentForm.querySelector('input[name="language"]').value);
    });
});
</script>
```

### Issue 3: Switches But Doesn't Change Language

**Symptoms:**
- Cookie changes
- Page reloads
- But language stays the same

**Possible Causes:**
1. **Translation files missing**
   - Check `/locale/vi/LC_MESSAGES/django.mo` exists

2. **Strings not translated**
   - Only `{% trans %}` tags will change

3. **Cache issue**
   - Browser or Django caching old translations

**Fix:**
```bash
# Recompile translations
python manage.py compilemessages

# Clear Django cache
python manage.py shell -c "from django.core.cache import cache; cache.clear()"

# Restart server
python manage.py runserver
```

### Issue 4: URL Redirects to Wrong Page

**Symptoms:**
- Switches language
- But redirects to `/` instead of current page

**Possible Causes:**
1. **`next` parameter empty or wrong**
2. **i18n_patterns causing URL change**

**Fix:**
Check form has: `<input type="hidden" name="next" value="{{ request.path }}">`

---

## 🧪 Manual Test

Test the language switching manually using curl:

```bash
# Get CSRF token first
curl -c cookies.txt http://localhost:8000/dashboard/

# Extract CSRF token
# On Windows PowerShell:
$csrf = (Get-Content cookies.txt | Select-String "csrftoken").ToString().Split("`t")[-1]

# Switch to English
curl -b cookies.txt -c cookies.txt -X POST http://localhost:8000/i18n/setlang/ `
  -d "language=en" `
  -d "next=/dashboard/" `
  -d "csrfmiddlewaretoken=$csrf" `
  -H "Referer: http://localhost:8000/dashboard/"

# Check cookie
Get-Content cookies.txt | Select-String "django_language"

# Should show: django_language	en
```

---

## ✅ Verification Checklist

Run these checks:

```bash
# 1. Check settings
python manage.py shell -c "from django.conf import settings; print('Default Lang:', settings.LANGUAGE_CODE); print('Languages:', settings.LANGUAGES); print('Has LANGUAGE_COOKIE_SECURE:', hasattr(settings, 'LANGUAGE_COOKIE_SECURE'))"

# 2. Check middleware order
python manage.py shell -c "from django.conf import settings; mw = settings.MIDDLEWARE; sess = mw.index('django.contrib.sessions.middleware.SessionMiddleware'); locale = mw.index('django.middleware.locale.LocaleMiddleware'); print('Session before Locale:', sess < locale)"

# 3. Check i18n URL
python manage.py shell -c "from django.urls import reverse; print('setlang URL:', reverse('set_language'))"

# 4. Test activation
python manage.py shell -c "from django.utils.translation import activate, get_language; activate('en'); print('After EN:', get_language()); activate('vi'); print('After VI:', get_language())"

# 5. Check translation files
python manage.py shell -c "import os; from django.conf import settings; locale_dir = settings.LOCALE_PATHS[0]; print('VI MO exists:', os.path.exists(os.path.join(locale_dir, 'vi/LC_MESSAGES/django.mo')))"
```

All should return expected values!

---

## 🔧 Nuclear Option: Complete Reset

If nothing works, try this complete reset:

```bash
# 1. Stop server
Ctrl+C

# 2. Clear all Python cache
python -c "import os, shutil; [shutil.rmtree(os.path.join(root, d)) for root, dirs, _ in os.walk('.') for d in dirs if d == '__pycache__']"

# 3. Clear cookies in browser
# Go to: chrome://settings/siteData
# Search: localhost
# Click: Clear all site data

# 4. Restart server
python manage.py runserver

# 5. Open in incognito/private window
# Navigate to: http://localhost:8000
```

---

## 📊 Debug Output Analysis

When you click the language switch, you should see this flow:

### Console Output:
```
1. Current URL: http://localhost:8000/dashboard/
2. Language cookie: django_language=vi
3. Language form submitted
4. Action: /i18n/setlang/
5. Language: en
6. Next: /dashboard/
```

### Network Tab:
```
Request URL: http://localhost:8000/i18n/setlang/
Request Method: POST
Status Code: 302 Found
Location: /dashboard/

Form Data:
  csrfmiddlewaretoken: [long token]
  language: en
  next: /dashboard/

Response Headers:
  Set-Cookie: django_language=en; Max-Age=31536000; Path=/; SameSite=Lax
```

### Application Tab (Cookies):
```
Name: django_language
Value: en
Domain: localhost
Path: /
Expires: [1 year from now]
Size: 19
HttpOnly: ✗
Secure: ✗
SameSite: Lax
```

---

## 🚨 Emergency: Direct Database Check

If the issue persists, check if it's a browser-specific issue:

1. **Try different browser**
   - Chrome
   - Firefox
   - Edge

2. **Try incognito/private mode**
   - Eliminates extension interference

3. **Try different device**
   - Phone browser
   - Different computer

4. **Check if it's URL-specific**
   - Try switching on login page
   - Try switching on dashboard
   - Try switching on different pages

---

## 📝 Report Template

If you need to report the issue, use this template:

```
**Browser:** Chrome 120 / Firefox 121 / etc
**OS:** Windows 11 / macOS / Linux
**Python Version:** python --version
**Django Version:** pip show django

**Steps to reproduce:**
1. Open http://localhost:8000
2. Login as: [username]
3. Click language dropdown
4. Click "English"

**Expected:** Page reloads in English
**Actual:** [What actually happens]

**Console Errors:** [Copy from DevTools Console]
**Network Tab:** [Screenshot of /i18n/setlang/ request]
**Cookies:** [Screenshot of cookies]

**Already tried:**
- [ ] Cleared browser cookies
- [ ] Cleared Django cache
- [ ] Restarted server
- [ ] Tried incognito mode
- [ ] Tried different browser
```

---

## ✅ Success Criteria

Language switching is working correctly if:

1. ✅ Dropdown shows current language ("Tiếng Việt" or "English")
2. ✅ Clicking other language reloads page
3. ✅ Navigation items change language
4. ✅ Cookie `django_language` is set correctly
5. ✅ Language persists across page navigation
6. ✅ Language persists after browser restart
7. ✅ Both directions work (en→vi and vi→en)

---

## 🎯 Next Steps

If after all these steps it still doesn't work:

1. **Capture network traffic**
   ```bash
   # Use browser DevTools
   # Network tab → Preserve log
   # Try to switch language
   # Right-click request → Copy → Copy as cURL
   # Share the cURL command for analysis
   ```

2. **Enable Django debug logging**
   Add to settings.py:
   ```python
   LOGGING = {
       'version': 1,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
           },
       },
       'loggers': {
           'django.utils.translation': {
               'handlers': ['console'],
               'level': 'DEBUG',
           },
       },
   }
   ```

3. **Check Django version compatibility**
   ```bash
   pip show django
   # Should be Django 4.2.7 or later
   ```

---

**Remember:** The debug console logs and network tab are your best friends for diagnosing this issue!
