# Quick Test - Language Switching (Both Directions)

**2 MINUTE TEST** ⏱️

---

## ✅ What I Fixed

You said **English → Vietnamese didn't work**. I fixed it!

**Backend test proves both directions work perfectly:**
```
✅ English → Vietnamese: SUCCESS
✅ Vietnamese → English: SUCCESS
✅ Multiple switches: ALL OK
```

**Frontend fix applied:** Enhanced JavaScript that sets cookie immediately and forces cache bypass.

---

## 🚀 Test NOW (2 Steps)

### Step 1: Restart Server
```bash
python manage.py runserver
```

### Step 2: Test in Incognito Mode
```
Press: Ctrl+Shift+N (Chrome/Edge)
Open: http://localhost:8000
Press: F12 (open console)
```

---

## 🧪 What to Do

**You'll see:** `[en]` badge → English text

**Test 1: English → Vietnamese**
1. Click language dropdown
2. Click "Tiếng Việt"
3. Watch console and page

**Should happen:**
- Console shows: "Cookie set manually to: vi"
- Badge changes: `[en]` → `[vi]`
- Text changes: "Dashboard" → "Bảng điều khiển"

**Test 2: Vietnamese → English**
1. Click language dropdown
2. Click "English"
3. Watch console and page

**Should happen:**
- Console shows: "Cookie set manually to: en"
- Badge changes: `[vi]` → `[en]`
- Text changes: "Bảng điều khiển" → "Dashboard"

**Test 3: Switch 10 times**
- Switch back and forth rapidly
- Every switch should work
- No errors in console

---

## ✅ Success = All These Work

- [ ] Default is English `[en]`
- [ ] English → Vietnamese works
- [ ] Vietnamese → English works
- [ ] Can switch 10+ times
- [ ] Console shows "Cookie set manually to: ..."
- [ ] No red errors in console

**If ALL work:** ✅ **PERFECT!** 🎉

**If ANY fail:** ❌ Send screenshot of console!

---

## 🔍 What to Look For in Console

**Good (should see):**
```
=== LANGUAGE SWITCH ===
Switching to: vi
Cookie set manually to: vi
Response status: 200
Reloading to: /?lang=vi&nocache=...
=== PAGE LOADED ===
Language cookie: django_language=vi
```

**Bad (should NOT see):**
```
Error: ...
Failed to fetch ...
CSRF token missing ...
```

---

## 📊 Visual Check

**English `[en]`:**
- Dashboard
- Events
- Today's Tasks
- Focus Timer
- Analytics

**Vietnamese `[vi]`:**
- Bảng điều khiển
- Sự kiện
- Nhiệm vụ hôm nay
- Đồng hồ tập trung
- Phân tích

**Should be COMPLETELY DIFFERENT!** 🎨

---

## 🎯 Quick Checklist

1. ✅ Restart server
2. ✅ Open incognito (Ctrl+Shift+N)
3. ✅ Open console (F12)
4. ✅ Test English → Vietnamese
5. ✅ Test Vietnamese → English
6. ✅ Switch multiple times

**Total time: 2 minutes!** ⏱️

---

## 💡 If It Doesn't Work

**Check console for red errors**, then:

1. Take screenshot of console
2. Tell me what you see
3. I'll debug it immediately!

---

## 🎉 Bottom Line

**Both directions should work perfectly now!**

**The fix:**
- ✅ JavaScript sets cookie immediately
- ✅ Forces hard reload with cache bypass
- ✅ Adds timestamp to prevent caching
- ✅ Works in BOTH directions

**Test it now!** 🚀

---

**Backend tested ✅ Frontend fixed ✅ Ready to go ✅**
