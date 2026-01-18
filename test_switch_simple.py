"""
Test switching from Vietnamese to English - Simple version without Unicode
Run this with: python test_switch_simple.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')
django.setup()

from django.test import Client

# Create test client
client = Client()

print("=" * 60)
print("TESTING: Vietnamese to English Switch")
print("=" * 60)

# Step 1: Set language to Vietnamese first
print("\n1. Setting language to Vietnamese...")
response = client.post('/i18n/setlang/', {
    'language': 'vi',
    'next': '/dashboard/'
})
print(f"   Status: {response.status_code}")
cookie = client.cookies.get('django_language')
print(f"   django_language cookie: {cookie.value if cookie else 'Not set'}")

# Step 2: Try to switch back to English
print("\n2. Switching back to English...")
response = client.post('/i18n/setlang/', {
    'language': 'en',
    'next': '/dashboard/'
})
print(f"   Status: {response.status_code}")
print(f"   Location header: {response.get('Location', 'None')}")
cookie = client.cookies.get('django_language')
print(f"   django_language cookie: {cookie.value if cookie else 'Not set'}")

# Step 3: Check if cookie actually changed
print(f"\n3. Cookie value check:")
print(f"   Expected: 'en'")
print(f"   Actual: '{cookie.value if cookie else 'Not set'}'")
print(f"   Match: {cookie.value == 'en' if cookie else False}")

# Step 4: Final verification
print("\n4. Final verification:")
if cookie and cookie.value == 'en':
    print("   SUCCESS: Cookie updated to English")
else:
    print(f"   FAILED: Cookie is '{cookie.value if cookie else 'Not set'}', expected 'en'")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
