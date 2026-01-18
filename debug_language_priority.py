"""
Debug language detection priority
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')
django.setup()

from django.test import Client
from django.conf import settings

client = Client()

print("=" * 60)
print("DEBUG: Language Detection Priority")
print("=" * 60)

print("\n[SETTINGS]")
print(f"LANGUAGE_CODE (default): {settings.LANGUAGE_CODE}")
print(f"LANGUAGES: {settings.LANGUAGES}")
print(f"USE_I18N: {settings.USE_I18N}")

print("\n[MIDDLEWARE]")
for i, mw in enumerate(settings.MIDDLEWARE):
    if 'locale' in mw.lower() or 'session' in mw.lower():
        print(f"{i}. {mw}")

print("\n[TEST 1] Fresh client - no cookie, no session")
response = client.get('/')
print(f"Status: {response.status_code}")
print(f"Cookies: {dict(client.cookies)}")

print("\n[TEST 2] Set cookie to 'en'")
client.cookies['django_language'] = 'en'
response = client.get('/')
print(f"Cookie: django_language=en")
print(f"Status: {response.status_code}")

print("\n[TEST 3] Set cookie to 'vi'")
client.cookies['django_language'] = 'vi'
response = client.get('/')
print(f"Cookie: django_language=vi")
print(f"Status: {response.status_code}")

print("\n[TEST 4] Use setlang POST to set to 'en'")
client = Client()  # Fresh client
response = client.post('/i18n/setlang/', {
    'language': 'en',
    'next': '/'
})
print(f"POST response status: {response.status_code}")
print(f"Cookies after POST: {dict(client.cookies)}")

if hasattr(client.session, '_session'):
    print(f"Session data: {dict(client.session)}")

print("\n[TEST 5] Use setlang POST to set to 'vi'")
client = Client()
response = client.post('/i18n/setlang/', {
    'language': 'vi',
    'next': '/'
})
print(f"POST response status: {response.status_code}")
print(f"Cookies after POST: {dict(client.cookies)}")

if hasattr(client.session, '_session'):
    print(f"Session data: {dict(client.session)}")

print("\n" + "=" * 60)
