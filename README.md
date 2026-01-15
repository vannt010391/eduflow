# EduFlow AI - Smart Educational Planning Web Application

![EduFlow AI](https://img.shields.io/badge/Django-4.2.7-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

EduFlow AI is a smart educational planning web application designed to help students manage academic events and optimize their focus-break rhythm to improve learning effectiveness and reduce mental overload.

**Core Value Proposition:** "Not only managing time, but managing learning energy."

## Features

### 1. Event Edu Planner (Academic Event Management)
- Create, edit, and delete academic events (exams, quizzes, assignments, presentations, extracurricular activities)
- Automatic preparation schedule generation
- Progress tracking with deadline risk warnings
- Priority-based event organization

### 2. FocusBreak AI (Focus & Rest Optimization)
- Study session tracking with timer functionality
- Intelligent break recommendations based on:
  - Pomodoro (25/5)
  - Extended focus (45/10)
  - Deep work (60/15)
- Overload prevention alerts
- Consecutive session tracking

### 3. Analytics & Effectiveness Measurement
- Daily and weekly study metrics
- Event completion rate tracking
- Consistency score calculation
- Session duration analysis
- Visual progress indicators

### 4. Multilingual Support
- English and Vietnamese language options
- Easy language switching from navigation menu
- All UI elements fully translated
- Automatic language detection based on browser settings

## Technology Stack

- **Backend:** Django 4.2.7
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Forms:** Django Crispy Forms with Bootstrap 4
- **Icons:** Bootstrap Icons
- **Internationalization:** Django i18n (English and Vietnamese)

## Project Structure

```
eduflow_ai/
├── eduflow_ai/           # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                # User authentication and profiles
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── events/               # Academic event management
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── study_sessions/       # Study session tracking
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── focus_break/          # Focus timer and break recommendations
│   ├── models.py
│   ├── views.py
│   ├── utils.py
│   └── urls.py
├── analytics/            # Dashboard and analytics
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── templates/            # HTML templates
│   ├── base.html
│   ├── users/
│   ├── events/
│   ├── study_sessions/
│   ├── focus_break/
│   └── analytics/
└── static/               # Static files (CSS, JS)
    ├── css/
    └── js/
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Database Migrations

```bash
python manage.py migrate
```

### Step 3: Populate Initial Data

```bash
python manage.py populate_focus_models
```

This will create the three default focus models:
- Pomodoro (25 min focus / 5 min break)
- Extended Focus (45 min focus / 10 min break)
- Deep Work (60 min focus / 15 min break)

### Step 4: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 5: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage Guide

### For Students

#### 1. Registration & Login
- Navigate to `/users/register/` to create a new account
- Login at `/users/login/`

#### 2. Create an Event
1. Go to "Events" in the navigation
2. Click "Create New Event"
3. Fill in the event details:
   - Title (e.g., "Midterm Exam - Mathematics")
   - Event type (Exam, Quiz, Assignment, etc.)
   - Event date and time
   - Subject/category
   - Priority level (Low, Medium, High)
   - Estimated preparation time in hours
   - Optional description
4. Click "Create Event"

**The system will automatically:**
- Calculate available days until the event
- Split preparation time into manageable study sessions
- Distribute sessions evenly across available days
- Create a personalized study schedule

#### 3. Manage Study Sessions
- View today's sessions from the dashboard
- Start a session timer
- Mark sessions as completed, skipped, or postponed
- Track actual study time vs. planned time

#### 4. Use Focus Timer
1. Navigate to "Focus Timer"
2. Choose a focus model (Pomodoro, Extended, or Deep Work)
3. Click "Start" to begin a focus session
4. The system will recommend break duration based on:
   - Number of consecutive sessions
   - Total daily study time
   - Your preferences

#### 5. View Analytics
- Access the Analytics Dashboard to see:
  - Daily and weekly study metrics
  - Event completion rates
  - Consistency scores
  - Session duration trends
  - Events at risk

### For Administrators

Access the Django admin panel at `/admin/` to:
- Manage users
- View all events and sessions
- Monitor focus session data
- Access analytics logs

## Database Models

### Event
- Stores academic events with automatic schedule generation
- Tracks completion percentage and risk status

### StudySession
- Individual study sessions linked to events
- Tracks both planned and actual study time

### FocusSession
- Records focus timer sessions
- Links to study sessions when applicable

### BreakSession
- Tracks break periods between focus sessions

### UserProfile
- Extended user information (student ID, grade level, bio)

### UserPreference
- User-specific settings for focus models and daily limits

### DailyStudyLog & WeeklyStudyLog
- Aggregate analytics data for performance tracking

## Key Features Explained

### Automatic Schedule Generation
When you create an event, the system:
1. Calculates days remaining until the event
2. Determines optimal session duration (25-60 minutes)
3. Calculates number of sessions needed
4. Distributes sessions across available days
5. Assigns default start times (customizable)

### Intelligent Break Recommendations
The system recommends breaks based on:
- **Standard break:** After 1 session
- **Medium break:** After 2 consecutive sessions
- **Long break:** After 4 consecutive sessions
- **Extended break:** When daily study limit is reached

### Risk Detection
Events are flagged as "at risk" when:
- Less than 2 days remaining with <50% completion
- Less than 1 day remaining with <80% completion

## Customization

### Change Language
1. Click on the "Language" dropdown in the navigation menu
2. Select your preferred language:
   - **English** - Full English interface
   - **Tiếng Việt** - Vietnamese interface
3. The page will reload with your selected language
4. Your language preference is saved for future sessions

### Change Focus Preferences
1. Go to your profile dropdown
2. Click "Preferences"
3. Adjust:
   - Default focus model
   - Daily study limit
   - Overload alert settings

### Update Profile
1. Click on your username in the navigation
2. Select "Profile"
3. Edit student ID, grade level, and bio

## API Endpoints (URL Routes)

### User Routes
- `/users/register/` - User registration
- `/users/login/` - User login
- `/users/logout/` - User logout
- `/users/profile/` - User profile management

### Event Routes
- `/events/` - List all events
- `/events/<id>/` - Event detail
- `/events/create/` - Create new event
- `/events/<id>/update/` - Update event
- `/events/<id>/delete/` - Delete event

### Study Session Routes
- `/sessions/` - List all sessions
- `/sessions/<id>/` - Session detail
- `/sessions/<id>/start/` - Start session timer
- `/sessions/<id>/complete/` - Mark session complete
- `/sessions/<id>/skip/` - Skip session
- `/sessions/today/` - Today's sessions

### Focus Timer Routes
- `/focus/timer/` - Focus timer interface
- `/focus/start/` - Start focus session
- `/focus/end/<id>/` - End focus session
- `/focus/break/start/` - Start break
- `/focus/break/end/<id>/` - End break
- `/focus/preferences/` - Focus preferences

### Dashboard Routes
- `/dashboard/home/` - Main dashboard
- `/dashboard/` - Analytics dashboard

## Troubleshooting

### Static Files Not Loading
Run:
```bash
python manage.py collectstatic
```

### Database Issues
Delete `db.sqlite3` and run:
```bash
python manage.py migrate
python manage.py populate_focus_models
python manage.py createsuperuser
```

### Port Already in Use
Run on a different port:
```bash
python manage.py runserver 8080
```

## Future Enhancements (Not in MVP)

- AI-based adaptive focus modeling using ML
- Teacher/admin dashboards for classroom management
- Mobile application (iOS/Android)
- External calendar integration (Google Calendar, Outlook)
- LMS integration (Canvas, Blackboard, Moodle)
- Cloud database migration (PostgreSQL)
- Real-time notifications and reminders
- Collaborative study groups
- Gamification features (badges, achievements)

## Contributing

This is an MVP (Minimum Viable Product) designed for educational purposes. Contributions are welcome!

## License

MIT License - Feel free to use this project for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django documentation at https://docs.djangoproject.com/
3. Check Bootstrap documentation at https://getbootstrap.com/

## Success Metrics

EduFlow AI is considered successful if:
- Users can clearly see daily study tasks
- Events are completed on time more frequently
- Average focus session length becomes more balanced
- Users report reduced last-minute studying behavior

---

**Built with Django | Powered by Smart Learning Algorithms**
