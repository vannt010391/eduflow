"""
Test Django's language detection with cookie
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')
django.setup()

from django.test import Client
from django.utils.translation import get_language

# Create test client
client = Client()

print("=" * 60)
print("Testing Django Language Detection")
print("=" * 60)

# Test 1: Set cookie and make request
print("\n[TEST 1] Setting Vietnamese cookie and making request")
print("-" * 60)

# Set cookie to Vietnamese
client.cookies['django_language'] = 'vi'
print(f"Cookie set: django_language=vi")

# Make a request
response = client.get('/dashboard/')
print(f"Request to: /dashboard/")
print(f"Response status: {response.status_code}")

# Check what language Django detected
# We need to check in the template context
print(f"\nChecking response content for language indicators...")

# Check if Vietnamese text is in response
if 'Bảng điều khiển' in response.content.decode('utf-8', errors='ignore'):
    print("✅ FOUND Vietnamese text: 'Bảng điều khiển'")
    print("   Django IS reading the cookie correctly!")
else:
    print("❌ NOT FOUND Vietnamese text")
    print("   Django is NOT reading the cookie!")

if 'Dashboard' in response.content.decode('utf-8', errors='ignore'):
    print("   Found English text: 'Dashboard'")
    print("   Django is showing English despite vi cookie!")

# Test 2: Use Django's setlang view
print("\n[TEST 2] Using Django's set_language view")
print("-" * 60)

response = client.post('/i18n/setlang/', {
    'language': 'vi',
    'next': '/dashboard/'
})
print(f"POST to /i18n/setlang/ with language=vi")
print(f"Response status: {response.status_code}")
print(f"Cookie after: {client.cookies.get('django_language').value if client.cookies.get('django_language') else 'Not set'}")

# Follow redirect
if response.status_code in [301, 302]:
    redirect_url = response.url
    print(f"Following redirect to: {redirect_url}")
    response = client.get(redirect_url)
    print(f"Response status: {response.status_code}")

    # Check content
    content = response.content.decode('utf-8', errors='ignore')
    if 'Bảng điều khiển' in content:
        print("✅ FOUND Vietnamese text after redirect!")
    else:
        print("❌ Still showing English after redirect!")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
