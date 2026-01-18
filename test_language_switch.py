#!/usr/bin/env python
"""
Test language switching functionality.
Run this script to check if language switching works correctly.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')
django.setup()

from django.conf import settings
from django.utils.translation import get_language, activate

print("=" * 60)
print("LANGUAGE SWITCHING TEST")
print("=" * 60)

print("\n1. Settings Check:")
print(f"   Default Language: {settings.LANGUAGE_CODE}")
print(f"   Available Languages: {settings.LANGUAGES}")
print(f"   Locale Paths: {settings.LOCALE_PATHS}")
print(f"   USE_I18N: {settings.USE_I18N}")

print("\n2. Cookie Settings:")
print(f"   Cookie Name: {settings.LANGUAGE_COOKIE_NAME}")
print(f"   Cookie Age: {settings.LANGUAGE_COOKIE_AGE} seconds ({settings.LANGUAGE_COOKIE_AGE / (60*60*24)} days)")
print(f"   Cookie Path: {settings.LANGUAGE_COOKIE_PATH}")
print(f"   Cookie Secure: {settings.LANGUAGE_COOKIE_SECURE}")
print(f"   Cookie SameSite: {settings.LANGUAGE_COOKIE_SAMESITE}")

print("\n3. Middleware Check:")
has_session = 'django.contrib.sessions.middleware.SessionMiddleware' in settings.MIDDLEWARE
has_locale = 'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE
print(f"   Session Middleware: {'✓' if has_session else '✗'}")
print(f"   Locale Middleware: {'✓' if has_locale else '✗'}")

if has_session and has_locale:
    session_idx = settings.MIDDLEWARE.index('django.contrib.sessions.middleware.SessionMiddleware')
    locale_idx = settings.MIDDLEWARE.index('django.middleware.locale.LocaleMiddleware')
    print(f"   Middleware Order: {'✓ Correct' if session_idx < locale_idx else '✗ WRONG'}")

print("\n4. Context Processor Check:")
context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
has_i18n = 'django.template.context_processors.i18n' in context_processors
print(f"   i18n Context Processor: {'✓' if has_i18n else '✗'}")

print("\n5. URL Configuration Check:")
from django.urls import reverse
try:
    setlang_url = reverse('set_language')
    print(f"   set_language URL: ✓ {setlang_url}")
except:
    print(f"   set_language URL: ✗ NOT FOUND")

print("\n6. Language Activation Test:")
print(f"   Current Language: {get_language()}")

activate('en')
print(f"   After activate('en'): {get_language()}")

activate('vi')
print(f"   After activate('vi'): {get_language()}")

print("\n7. Translation Files Check:")
import os
locale_dir = settings.LOCALE_PATHS[0]
print(f"   Locale Directory: {locale_dir}")
print(f"   Directory Exists: {'✓' if os.path.exists(locale_dir) else '✗'}")

if os.path.exists(locale_dir):
    for lang_code, lang_name in settings.LANGUAGES:
        lang_dir = os.path.join(locale_dir, lang_code, 'LC_MESSAGES')
        po_file = os.path.join(lang_dir, 'django.po')
        mo_file = os.path.join(lang_dir, 'django.mo')
        print(f"   {lang_name} ({lang_code}):")
        print(f"      - PO file: {'✓' if os.path.exists(po_file) else '✗'}")
        print(f"      - MO file: {'✓' if os.path.exists(mo_file) else '✗'}")

print("\n8. i18n_patterns Check:")
from django.conf.urls.i18n import i18n_patterns
print(f"   i18n_patterns imported: ✓")
print(f"   prefix_default_language in urls.py: Check manually")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

print("\nDEBUGGING TIPS:")
print("1. Clear browser cookies and cache")
print("2. Check browser DevTools > Application > Cookies")
print("3. Look for 'django_language' cookie")
print("4. Check Network tab for POST to /i18n/setlang/")
print("5. Verify CSRF token is present in form")
print("\nIf switching still doesn't work, run:")
print("  python manage.py runserver")
print("  Then manually POST to /i18n/setlang/ with:")
print("    - language: en or vi")
print("    - next: /dashboard/")
print("    - csrfmiddlewaretoken: [from page]")
