# Phase 3 - UI Access Guide
## How to Access All New Features

**Last Updated:** 2026-01-16

---

## 🎯 Quick Access Summary

Phase 3 adds AI-enhanced features accessible from multiple locations in the UI:

1. **Navigation Menu** - "AI Features" dropdown (top right)
2. **Dashboard** - Two prominent widgets
3. **Event Detail Pages** - Diagnostic test upload
4. **Direct URLs** - For bookmarking

---

## 📍 1. Navigation Menu (Always Visible)

**Location:** Top navigation bar → "AI Features" dropdown

### New Menu Added
A new dropdown menu with a star icon (⭐) appears in the main navigation:

```
[Dashboard] [Events] [Today's Tasks] [Focus Timer] [Analytics] [★ AI Features ▼]
```

**Dropdown Items:**
1. **Log Emotional State** 😊
   - Quick access to emotional state logging form
   - URL: `/emotional/log/`

2. **Plan Suggestions** 💡
   - View all AI-generated plan adjustment suggestions
   - URL: `/diagnostics/suggestions/`

**How to Use:**
1. Click "AI Features" in the navigation
2. Select either option from the dropdown
3. Access anytime from any page

---

## 📊 2. Dashboard Widgets

**Location:** Dashboard → After daily metrics, before event statistics

### Widget 1: Emotional State
**Title:** "How are you feeling today?" 😊

**Features:**
- Shows last logged state if already logged today
- Displays energy/stress/focus levels with icons
- Privacy notice
- "Log Your State" button

**If Not Logged Today:**
```
┌─────────────────────────────────┐
│ How are you feeling today? 😊   │
├─────────────────────────────────┤
│ Help us optimize your study     │
│ plan by sharing how you're      │
│ feeling.                         │
│                                  │
│ 🛡️ Your data is private and    │
│ only used to improve your       │
│ study experience.                │
│                                  │
│     [Log Your State]             │
└─────────────────────────────────┘
```

**If Already Logged:**
```
┌─────────────────────────────────┐
│ How are you feeling today? 😊   │
├─────────────────────────────────┤
│ ✓ Last logged: 2 hours ago      │
│                                  │
│   ⚡ Medium    🌡️ High   👁️ Low │
│   Energy      Stress    Focus   │
│                                  │
│     [Log Your State]             │
└─────────────────────────────────┘
```

### Widget 2: AI Suggestions
**Title:** "AI Suggestions" 💡

**Features:**
- Shows count of pending suggestions
- Alert if suggestions exist
- "View Suggestions" or "View History" button

**If Pending Suggestions:**
```
┌─────────────────────────────────┐
│ AI Suggestions 💡                │
├─────────────────────────────────┤
│ ⚠️ 3 pending suggestions        │
│                                  │
│ AI has analyzed your recent     │
│ activity and diagnostic tests.  │
│ Review the suggestions to       │
│ optimize your study plan.       │
│                                  │
│  [View Suggestions (3)]         │
└─────────────────────────────────┘
```

**If No Suggestions:**
```
┌─────────────────────────────────┐
│ AI Suggestions 💡                │
├─────────────────────────────────┤
│ ✓ No pending suggestions        │
│                                  │
│ AI will create suggestions      │
│ based on:                        │
│ • Your emotional state           │
│ • Diagnostic test results        │
│ • Study session patterns         │
│                                  │
│    [View History]                │
└─────────────────────────────────┘
```

---

## 📅 3. Event Detail Pages

**Location:** Events → Select an event → Diagnostic Test card (left sidebar)

### New Card: Diagnostic Test
**Location:** Left sidebar, below "Days Remaining"

**Features:**
- Upload diagnostic test button (if none exists)
- View test details (if already uploaded)
- Shows score percentage and analysis status

**If No Test Uploaded:**
```
┌─────────────────────────────────┐
│ 📋 Diagnostic Test               │
├─────────────────────────────────┤
│ Upload a diagnostic test to     │
│ identify your weak areas and    │
│ get personalized review         │
│ suggestions.                     │
│                                  │
│  [Upload Diagnostic Test]       │
└─────────────────────────────────┘
```

**If Test Uploaded:**
```
┌─────────────────────────────────┐
│ 📋 Diagnostic Test               │
├─────────────────────────────────┤
│ ✓ Test uploaded:                │
│   Physics Practice Test         │
│                                  │
│      70%        [Analyzed]      │
│   14/20 correct                  │
│                                  │
│   [View Test Details]           │
└─────────────────────────────────┘
```

---

## 🔗 4. Direct URLs (For Bookmarking)

### Emotional State
- **Log Form:** `http://127.0.0.1:8000/emotional/log/`
- **Submit:** `http://127.0.0.1:8000/emotional/log/submit/` (POST only)

### Diagnostic Tests
- **Upload Test:** `http://127.0.0.1:8000/diagnostics/upload/<event_id>/`
- **View Test:** `http://127.0.0.1:8000/diagnostics/test/<test_id>/`
- **Add Question:** `http://127.0.0.1:8000/diagnostics/test/<test_id>/add-question/`
- **Analyze Test:** `http://127.0.0.1:8000/diagnostics/test/<test_id>/analyze/` (POST only)

### Plan Suggestions
- **List (All):** `http://127.0.0.1:8000/diagnostics/suggestions/`
- **List (Pending):** `http://127.0.0.1:8000/diagnostics/suggestions/?status=pending`
- **List (Accepted):** `http://127.0.0.1:8000/diagnostics/suggestions/?status=accepted`
- **List (Rejected):** `http://127.0.0.1:8000/diagnostics/suggestions/?status=rejected`
- **View Suggestion:** `http://127.0.0.1:8000/diagnostics/suggestion/<suggestion_id>/`
- **Accept:** `http://127.0.0.1:8000/diagnostics/suggestion/<suggestion_id>/accept/` (POST only)
- **Reject:** `http://127.0.0.1:8000/diagnostics/suggestion/<suggestion_id>/reject/` (POST only)

---

## 🎬 Complete User Journeys

### Journey 1: Log Emotional State
1. **From Dashboard:**
   - See "How are you feeling today?" widget
   - Click "Log Your State" button
   - Fill in 3 sliders (energy, stress, focus)
   - Click "Submit"
   - Redirected to dashboard with confirmation

2. **From Navigation:**
   - Click "AI Features" → "Log Emotional State"
   - Fill in form
   - Submit
   - Return to dashboard

### Journey 2: Upload & Analyze Diagnostic Test
1. **Navigate to Event:**
   - Dashboard → Events → Select an event
   - See "Diagnostic Test" card in left sidebar

2. **Upload Test:**
   - Click "Upload Diagnostic Test"
   - Enter test title (e.g., "Physics Practice Test")
   - Optionally upload PDF
   - Click "Create Test"

3. **Add Questions:**
   - Enter question number
   - Enter question text
   - Enter correct answer
   - Enter your answer
   - Optionally add topic and error type
   - Click "Add & Add Another" (repeat for more questions)
   - OR click "Add & View Test" (when done)

4. **View & Analyze:**
   - See test detail page with all questions
   - See score percentage
   - Click "Analyze Test" button
   - AI analyzes errors and groups by topic
   - View error analysis results
   - See recommended review topics

### Journey 3: Review & Accept Plan Suggestions
1. **Navigate to Suggestions:**
   - Dashboard → See "3 pending suggestions" in AI Suggestions widget
   - Click "View Suggestions (3)"
   - OR Navigation → "AI Features" → "Plan Suggestions"

2. **View Suggestion List:**
   - See list of pending suggestions
   - Filter by status (pending/accepted/rejected/all)
   - Click on a suggestion to view details

3. **Review Suggestion:**
   - See context (emotional state, diagnostic results)
   - Read proposed adjustments (shorten, split, reorder, etc.)
   - Read AI rationale explaining why

4. **Make Decision:**
   - **To Accept:**
     - Optionally add notes
     - Click "Accept Adjustments"
     - System updates status
     - Redirected to suggestions list
   - **To Reject:**
     - Optionally add reason
     - Click "Reject Adjustments"
     - System updates status
     - Redirected to suggestions list

---

## 🎨 Visual Navigation Map

```
Main Navigation Bar
├── Dashboard
│   └── Widgets:
│       ├── Emotional State Widget → Log Form
│       └── AI Suggestions Widget → Suggestions List
│
├── Events
│   └── Event Detail
│       └── Diagnostic Test Card → Upload/View Test
│
└── ★ AI Features (NEW!)
    ├── Log Emotional State → Emotional State Form
    └── Plan Suggestions → Suggestions List
```

---

## ✅ Features Verification Checklist

Use this checklist to verify all UI access points work:

### Navigation Menu
- [ ] "AI Features" dropdown appears in navigation
- [ ] "Log Emotional State" opens emotional state form
- [ ] "Plan Suggestions" opens suggestions list

### Dashboard
- [ ] Emotional state widget appears
- [ ] Shows last logged state if available
- [ ] "Log Your State" button works
- [ ] AI suggestions widget appears
- [ ] Shows pending count if suggestions exist
- [ ] "View Suggestions" button works

### Event Detail
- [ ] Diagnostic test card appears in sidebar
- [ ] "Upload Diagnostic Test" button works (if no test)
- [ ] "View Test Details" button works (if test exists)
- [ ] Shows score and status correctly

### Emotional State Flow
- [ ] Form displays with 3 radio button groups
- [ ] Can select energy/stress/focus levels
- [ ] "Submit" saves state and redirects
- [ ] "Skip for Now" redirects without saving
- [ ] Warning message if needs_attention

### Diagnostic Test Flow
- [ ] Upload page shows form
- [ ] Can enter title and upload PDF
- [ ] Redirects to add question page
- [ ] Question form has all fields
- [ ] "Add & Add Another" adds and stays on form
- [ ] "Add & View Test" adds and shows test detail
- [ ] Test detail shows all questions
- [ ] Shows score percentage correctly
- [ ] "Analyze Test" button triggers analysis
- [ ] Analysis results display after analysis

### Suggestions Flow
- [ ] List page shows all suggestions
- [ ] Can filter by status (tabs work)
- [ ] Detail page shows context
- [ ] Shows all adjustments
- [ ] Shows rationale
- [ ] Accept form works
- [ ] Reject form works
- [ ] Status updates correctly

---

## 🚨 Common Issues & Solutions

### Issue: Can't find "AI Features" menu
**Solution:** Make sure you're logged in. The menu only appears for authenticated users.

### Issue: Emotional state form says "already logged today"
**Solution:** You can only log once per day. The message appears if you've already logged today.

### Issue: "Upload Diagnostic Test" button not working
**Solution:** Check that the URL pattern includes the event ID. Should be `/diagnostics/upload/<event_id>/`

### Issue: Dashboard widgets not showing Phase 3 features
**Solution:**
1. Check migrations are applied: `python manage.py migrate`
2. Verify apps added to INSTALLED_APPS
3. Check analytics view includes Phase 3 context

### Issue: Getting 404 on diagnostic URLs
**Solution:** Verify URLs are included in main urls.py:
```python
path('emotional/', include('emotional_state.urls')),
path('diagnostics/', include('diagnostics.urls')),
```

---

## 📱 Mobile Responsive Notes

All Phase 3 features are mobile-responsive:
- Navigation dropdown works on mobile
- Dashboard widgets stack vertically
- Forms are touch-friendly
- Cards adapt to screen size
- All buttons are large enough for touch

---

## 🎓 User Training Tips

### For First-Time Users:
1. **Start with Emotional State:**
   - Easy, quick (30 seconds)
   - Helps users understand the feature
   - No prerequisites needed

2. **Then Try Diagnostic Test:**
   - Upload a past test
   - Add 3-5 questions to see how it works
   - Analyze to see AI in action

3. **Wait for Suggestions:**
   - System generates suggestions based on data
   - Review when they appear
   - Start with accepting simple suggestions

### For Power Users:
- Use navigation menu for quick access
- Bookmark direct URLs for frequent tasks
- Check dashboard daily for new suggestions
- Upload diagnostic tests regularly for best results

---

## 📊 Analytics & Monitoring

Track feature usage via:
1. **Dashboard visits** - See if users notice widgets
2. **Emotional state logs** - Count per user per day
3. **Diagnostic tests** - Upload rate per event
4. **Suggestion acceptance rate** - % accepted vs rejected

---

## ✨ Next Steps

After verifying all access points:
1. Create user onboarding tour
2. Add tooltips for new users
3. Create video tutorials
4. Add in-app help text
5. Monitor user feedback

---

**Status:** All Phase 3 features are accessible via UI ✅

**Quick Test:**
1. Login → See "AI Features" in nav? ✅
2. Dashboard → See 2 new widgets? ✅
3. Event detail → See "Diagnostic Test" card? ✅

**All access points working!** 🎉
