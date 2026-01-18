"""
Test Claude API Configuration and Connection
"""
import os
import sys
import codecs

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from django.conf import settings
from dotenv import load_dotenv

# Reload .env to get latest values
load_dotenv(override=True)

print("="*70)
print(" CLAUDE API CONFIGURATION TEST")
print("="*70)

# Test 1: Check Environment Variables
print("\n[TEST 1] Environment Variables")
print("-"*70)

ai_enabled = os.getenv('AI_ENABLED')
ai_provider = os.getenv('AI_PROVIDER')
ai_api_key = os.getenv('AI_API_KEY')
ai_model = os.getenv('AI_MODEL')

print(f"AI_ENABLED: {ai_enabled}")
print(f"AI_PROVIDER: {ai_provider}")
print(f"AI_MODEL: {ai_model}")

if ai_api_key:
    # Mask API key for security
    masked_key = ai_api_key[:15] + "..." + ai_api_key[-4:] if len(ai_api_key) > 20 else "***"
    print(f"AI_API_KEY: {masked_key} (length: {len(ai_api_key)} chars)")
else:
    print(f"AI_API_KEY: Not set ❌")

# Validate configuration
if ai_provider != 'anthropic':
    print("\n⚠️  WARNING: AI_PROVIDER is not 'anthropic'")
    print("   Set AI_PROVIDER=anthropic in your .env file to use Claude")
    print("   Current provider:", ai_provider)

if not ai_api_key or ai_api_key == 'your-api-key-here' or ai_api_key == '':
    print("\n❌ ERROR: API key not configured")
    print("   Please set AI_API_KEY in your .env file")
    print("   Get your key from: https://console.anthropic.com/")
    sys.exit(1)

if not ai_api_key.startswith('sk-ant-'):
    print("\n⚠️  WARNING: API key format looks incorrect")
    print("   Anthropic keys should start with 'sk-ant-'")
    print("   Your key starts with:", ai_api_key[:10])

print("\n✅ Environment variables loaded")

# Test 2: Check Anthropic SDK Installation
print("\n[TEST 2] Anthropic SDK Installation")
print("-"*70)

try:
    import anthropic
    print(f"✅ Anthropic SDK installed")
    print(f"   Version: {anthropic.__version__}")

    # Check minimum version
    min_version = "0.18.0"
    current_version = anthropic.__version__
    print(f"   Required: >= {min_version}")

    if current_version >= min_version:
        print(f"   ✅ Version check passed")
    else:
        print(f"   ⚠️  Version might be too old")

except ImportError as e:
    print(f"❌ Anthropic SDK not installed")
    print(f"   Error: {e}")
    print(f"   Install with: pip install anthropic>=0.18.0")
    sys.exit(1)

# Test 3: Django Settings
print("\n[TEST 3] Django Settings")
print("-"*70)

print(f"AI_ENABLED (Django): {settings.AI_ENABLED}")
print(f"AI_PROVIDER (Django): {settings.AI_PROVIDER}")
print(f"AI_MODEL (Django): {settings.AI_MODEL}")

if settings.AI_API_KEY:
    masked_key = settings.AI_API_KEY[:15] + "..." + settings.AI_API_KEY[-4:]
    print(f"AI_API_KEY (Django): {masked_key}")
else:
    print(f"AI_API_KEY (Django): Not set ❌")

print(f"AI_TIMEOUT: {settings.AI_TIMEOUT}s")
print(f"AI_MAX_RETRIES: {settings.AI_MAX_RETRIES}")
print(f"AI_RETRY_DELAY: {settings.AI_RETRY_DELAY}s")

print("\n✅ Django settings loaded")

# Test 4: Test Anthropic Client Initialization
print("\n[TEST 4] Anthropic Client Initialization")
print("-"*70)

if ai_provider == 'anthropic' and ai_api_key and ai_api_key != 'your-api-key-here':
    try:
        client = anthropic.Anthropic(api_key=ai_api_key)
        print("✅ Anthropic client initialized successfully")

        # Test 5: Simple API Call (Optional - costs money!)
        print("\n[TEST 5] API Connection Test (OPTIONAL)")
        print("-"*70)
        print("⚠️  This test makes a real API call and will use credits")
        print("   Skip if you want to save money for actual usage")

        response = input("\n   Run API test? (y/N): ").strip().lower()

        if response == 'y':
            print("\n   Making test API call to Claude...")
            print("   (This will cost ~$0.001)")

            try:
                message = client.messages.create(
                    model=ai_model or "claude-3-5-sonnet-20241022",
                    max_tokens=50,
                    messages=[
                        {"role": "user", "content": "Say 'Hello from EduFlow!' in exactly 5 words."}
                    ]
                )

                response_text = message.content[0].text
                print(f"\n   ✅ API call successful!")
                print(f"   Response: {response_text}")
                print(f"   Model used: {message.model}")
                print(f"   Usage:")
                print(f"     - Input tokens: {message.usage.input_tokens}")
                print(f"     - Output tokens: {message.usage.output_tokens}")

                # Calculate cost (Claude 3.5 Sonnet pricing)
                input_cost = message.usage.input_tokens * 3 / 1_000_000
                output_cost = message.usage.output_tokens * 15 / 1_000_000
                total_cost = input_cost + output_cost

                print(f"     - Cost: ${total_cost:.6f} (~{total_cost * 23000:.0f} VND)")

            except anthropic.AuthenticationError:
                print("\n   ❌ Authentication failed")
                print("   Your API key is invalid or expired")
                print("   Get a new key from: https://console.anthropic.com/")

            except anthropic.PermissionDeniedError:
                print("\n   ❌ Permission denied")
                print("   Possible reasons:")
                print("   - Insufficient credits")
                print("   - Payment method not added")
                print("   - Account not activated")
                print("   Check: https://console.anthropic.com/settings/billing")

            except anthropic.RateLimitError:
                print("\n   ❌ Rate limit exceeded")
                print("   You're making too many requests")
                print("   Wait a few minutes and try again")

            except anthropic.APIError as e:
                print(f"\n   ❌ API error: {e}")
                print(f"   Status code: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")

            except Exception as e:
                print(f"\n   ❌ Unexpected error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("\n   ⏭️  Skipped API test")
            print("   Configuration looks good, but not tested with real API")

    except Exception as e:
        print(f"❌ Failed to initialize Anthropic client")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()

else:
    print("⏭️  Skipped (not using Anthropic provider or API key not set)")

# Summary
print("\n" + "="*70)
print(" TEST SUMMARY")
print("="*70)

summary = []

# Check each requirement
if ai_provider == 'anthropic':
    summary.append("✅ Provider set to 'anthropic'")
else:
    summary.append(f"❌ Provider is '{ai_provider}' (should be 'anthropic')")

if ai_api_key and ai_api_key != 'your-api-key-here' and ai_api_key != '':
    summary.append("✅ API key configured")
else:
    summary.append("❌ API key not configured")

if ai_api_key and ai_api_key.startswith('sk-ant-'):
    summary.append("✅ API key format looks correct")
elif ai_api_key:
    summary.append("⚠️  API key format might be incorrect")

if 'anthropic' in sys.modules:
    summary.append("✅ Anthropic SDK installed")
else:
    summary.append("❌ Anthropic SDK not installed")

if ai_model and 'claude' in ai_model.lower():
    summary.append(f"✅ Model set to '{ai_model}'")
else:
    summary.append(f"⚠️  Model is '{ai_model}' (should be Claude model)")

for item in summary:
    print(item)

# Final verdict
print("\n" + "="*70)

all_pass = all("✅" in item for item in summary)

if all_pass:
    print("🎉 ALL CHECKS PASSED!")
    print("")
    print("Your Claude API is configured correctly!")
    print("")
    print("Next steps:")
    print("  1. Test in web UI: Create an event")
    print("  2. Verify study sessions are generated")
    print("  3. Check Anthropic dashboard for usage")
    print("  4. Monitor costs and quality")
    print("")
    print("Ready to use Claude for EduFlow AI! 🚀")
else:
    print("⚠️  SOME CHECKS FAILED")
    print("")
    print("Please fix the issues above before using Claude API")
    print("")
    print("Common fixes:")
    print("  - Set AI_PROVIDER=anthropic in .env")
    print("  - Add your API key to AI_API_KEY in .env")
    print("  - Get API key from: https://console.anthropic.com/")
    print("  - Install SDK: pip install anthropic>=0.18.0")
    print("")
    print("See: CLAUDE_API_SETUP.md for detailed instructions")

print("="*70)
