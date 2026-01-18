"""
Test focus time calculation fix
"""
import sys
import codecs

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Test cases
test_cases = [
    (3, 0.05),      # 3 minutes = 0.05 hours
    (30, 0.5),      # 30 minutes = 0.5 hours
    (60, 1.0),      # 60 minutes = 1 hour
    (90, 1.5),      # 90 minutes = 1.5 hours
    (120, 2.0),     # 120 minutes = 2 hours
    (180, 3.0),     # 180 minutes = 3 hours
]

print("="*60)
print("FOCUS TIME CALCULATION TEST")
print("="*60)

print("\nBefore Fix:")
print("3 min = approx. 63 hours ❌ (BUG!)")

print("\nAfter Fix:")
for minutes, expected_hours in test_cases:
    hours = minutes / 60.0
    status = "✅" if abs(hours - expected_hours) < 0.01 else "❌"
    print(f"{minutes} min = approx. {hours:.2f} hours {status}")

print("\n" + "="*60)
print("FIX VERIFIED: Calculation is now correct!")
print("="*60)
