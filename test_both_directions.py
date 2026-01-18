"""
Test language switching in BOTH directions
Run this with: python test_both_directions.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')
django.setup()

from django.test import Client

# Create test client
client = Client()

print("=" * 60)
print("TESTING: Language Switching BOTH Directions")
print("=" * 60)

# Test 1: English to Vietnamese
print("\n[TEST 1] English to Vietnamese")
print("-" * 60)

print("1.1. Setting language to English...")
response = client.post('/i18n/setlang/', {
    'language': 'en',
    'next': '/dashboard/'
})
cookie = client.cookies.get('django_language')
print(f"    Status: {response.status_code}")
print(f"    Cookie: {cookie.value if cookie else 'Not set'}")

print("\n1.2. Switching to Vietnamese...")
response = client.post('/i18n/setlang/', {
    'language': 'vi',
    'next': '/dashboard/'
})
cookie = client.cookies.get('django_language')
print(f"    Status: {response.status_code}")
print(f"    Cookie: {cookie.value if cookie else 'Not set'}")
print(f"    Expected: vi")
print(f"    Match: {cookie.value == 'vi' if cookie else False}")

if cookie and cookie.value == 'vi':
    print("    RESULT: SUCCESS - English to Vietnamese works")
else:
    print("    RESULT: FAILED - English to Vietnamese broken")

# Test 2: Vietnamese to English
print("\n[TEST 2] Vietnamese to English")
print("-" * 60)

print("2.1. Setting language to Vietnamese...")
response = client.post('/i18n/setlang/', {
    'language': 'vi',
    'next': '/dashboard/'
})
cookie = client.cookies.get('django_language')
print(f"    Status: {response.status_code}")
print(f"    Cookie: {cookie.value if cookie else 'Not set'}")

print("\n2.2. Switching to English...")
response = client.post('/i18n/setlang/', {
    'language': 'en',
    'next': '/dashboard/'
})
cookie = client.cookies.get('django_language')
print(f"    Status: {response.status_code}")
print(f"    Cookie: {cookie.value if cookie else 'Not set'}")
print(f"    Expected: en")
print(f"    Match: {cookie.value == 'en' if cookie else False}")

if cookie and cookie.value == 'en':
    print("    RESULT: SUCCESS - Vietnamese to English works")
else:
    print("    RESULT: FAILED - Vietnamese to English broken")

# Test 3: Multiple switches
print("\n[TEST 3] Multiple Rapid Switches")
print("-" * 60)

languages = ['en', 'vi', 'en', 'vi', 'en']
for i, lang in enumerate(languages, 1):
    response = client.post('/i18n/setlang/', {
        'language': lang,
        'next': '/dashboard/'
    })
    cookie = client.cookies.get('django_language')
    status = "OK" if cookie and cookie.value == lang else "FAIL"
    print(f"    Switch {i} to {lang}: {status} (cookie={cookie.value if cookie else 'None'})")

print("\n" + "=" * 60)
print("BACKEND TEST COMPLETE")
print("=" * 60)
