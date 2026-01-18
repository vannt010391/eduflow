"""
Test switching from Vietnamese to English specifically.
Run this with: python test_vi_to_en_switch.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create test client
client = Client()

print("=" * 60)
print("TESTING: Vietnamese → English Switch")
print("=" * 60)

# Step 1: Set language to Vietnamese first
print("\n1. Setting language to Vietnamese...")
response = client.post('/i18n/setlang/', {
    'language': 'vi',
    'next': '/dashboard/'
})
print(f"   Status: {response.status_code}")
print(f"   Cookies: {client.cookies}")
print(f"   django_language cookie: {client.cookies.get('django_language')}")

# Step 2: Make a request to verify we're in Vietnamese
print("\n2. Checking current language...")
from django.utils.translation import get_language, activate
activate('vi')
print(f"   Activated language: {get_language()}")

# Step 3: Try to switch back to English
print("\n3. Switching back to English...")
response = client.post('/i18n/setlang/', {
    'language': 'en',
    'next': '/dashboard/'
})
print(f"   Status: {response.status_code}")
print(f"   Location header: {response.get('Location', 'None')}")
print(f"   Cookies after: {client.cookies}")
print(f"   django_language cookie: {client.cookies.get('django_language')}")

# Step 4: Check if cookie actually changed
vi_value = client.cookies.get('django_language')
print(f"\n4. Cookie value check:")
print(f"   Expected: 'en'")
print(f"   Actual: '{vi_value.value if vi_value else 'Not set'}'")
print(f"   Match: {vi_value.value == 'en' if vi_value else False}")

# Step 5: Test with explicit cookie check
print("\n5. Final verification:")
if vi_value and vi_value.value == 'en':
    print("   ✅ SUCCESS: Cookie updated to English")
else:
    print(f"   ❌ FAILED: Cookie is '{vi_value.value if vi_value else 'Not set'}', expected 'en'")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
