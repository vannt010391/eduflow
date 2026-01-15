# EduFlow AI - Multilingual Support Guide

## Overview

EduFlow AI now supports both **English** and **Vietnamese** (Tiếng Việt) languages. Users can easily switch between languages using the navigation menu.

## Features

- ✅ Full English and Vietnamese translations
- ✅ Language switcher in navigation menu
- ✅ Session-based language persistence
- ✅ All UI elements translated including:
  - Navigation menu
  - Dashboard
  - Events management
  - Study sessions
  - Focus timer
  - Analytics
  - Forms and buttons
  - Messages and notifications

## How to Use

### Switching Languages

1. **Locate the Language Menu**: Click on the "Language" (🌐) dropdown in the top navigation bar
2. **Select Your Language**:
   - Click "English" for English interface
   - Click "Tiếng Việt" for Vietnamese interface
3. **Automatic Reload**: The page will automatically reload with your selected language
4. **Persistent Selection**: Your language choice is saved in your session

### For Users

The language switcher is available:
- On all pages when logged in
- In the top navigation bar
- Next to the user profile dropdown

### Default Language

- The application defaults to **English**
- Browser language detection is enabled
- Vietnamese speakers will see Vietnamese interface if their browser is set to Vietnamese

## Technical Implementation

### Files Structure

```
eduflow_ai/
├── locale/                      # Translation files
│   ├── en/                      # English (source)
│   └── vi/                      # Vietnamese
│       └── LC_MESSAGES/
│           ├── django.po        # Translation source
│           └── django.mo        # Compiled translations
├── compile_translations.py      # Translation compiler script
└── templates/
    └── base.html               # Language switcher UI
```

### Configuration

**Settings (eduflow_ai/settings.py):**
```python
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('vi', 'Tiếng Việt'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',  # Language middleware
    ...
]
```

**URL Configuration (eduflow_ai/urls.py):**
```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    # All app URLs here
    prefix_default_language=False,
)
```

### Translation Coverage

**126 translated messages** including:

#### Navigation & Menu Items
- Dashboard, Events, Today's Tasks, Focus Timer, Analytics
- Profile, Preferences, Login, Logout, Register

#### Event Management
- Event types: Exam, Quiz, Assignment, Presentation, etc.
- Priority levels: Low, Medium, High
- Event details and forms

#### Study Sessions
- Session statuses: Pending, Completed, Skipped, Postponed
- Session actions and details

#### Focus Timer
- Focus models: Pomodoro, Extended Focus, Deep Work
- Timer controls and status messages

#### Analytics
- Metrics labels and descriptions
- Chart labels and statistics

#### Common Terms
- Actions: Create, Edit, Delete, Save, Cancel
- Time units: minutes, hours, days
- Status indicators and messages

## Adding New Translations

### For Developers

1. **Mark strings for translation in templates:**
   ```django
   {% load i18n %}
   <h1>{% trans "Dashboard" %}</h1>
   ```

2. **Mark strings in Python code:**
   ```python
   from django.utils.translation import gettext_lazy as _

   title = _("Event created successfully")
   ```

3. **Update translation file:**
   Edit `locale/vi/LC_MESSAGES/django.po`:
   ```po
   msgid "New Feature"
   msgstr "Tính năng mới"
   ```

4. **Compile translations:**
   ```bash
   python compile_translations.py
   ```

5. **Restart Django server:**
   The new translations will be loaded automatically.

### Translation File Format

Example from `django.po`:
```po
msgid "Dashboard"
msgstr "Bảng điều khiển"

msgid "Events"
msgstr "Sự kiện"

msgid "Focus Timer"
msgstr "Đồng hồ tập trung"
```

## Adding More Languages

To add support for another language (e.g., Spanish):

1. **Update settings.py:**
   ```python
   LANGUAGES = [
       ('en', 'English'),
       ('vi', 'Tiếng Việt'),
       ('es', 'Español'),  # Add new language
   ]
   ```

2. **Create locale directory:**
   ```bash
   mkdir -p locale/es/LC_MESSAGES
   ```

3. **Create translation file:**
   Copy `locale/vi/LC_MESSAGES/django.po` to `locale/es/LC_MESSAGES/django.po`
   and translate all `msgstr` values to Spanish.

4. **Compile translations:**
   Update `compile_translations.py` to include Spanish or run manually.

5. **Update language switcher:**
   Edit `templates/base.html` to add Spanish option:
   ```html
   <li>
       <form action="{% url 'set_language' %}" method="post" class="language-form">
           {% csrf_token %}
           <input type="hidden" name="language" value="es">
           <button type="submit" class="dropdown-item">Español</button>
       </form>
   </li>
   ```

## Troubleshooting

### Translations not appearing

1. **Check .mo file exists:**
   ```bash
   ls locale/vi/LC_MESSAGES/django.mo
   ```

2. **Recompile translations:**
   ```bash
   python compile_translations.py
   ```

3. **Restart Django server:**
   ```bash
   python manage.py runserver
   ```

4. **Clear browser cache:**
   Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

### Language not switching

1. **Check middleware order** in settings.py:
   `LocaleMiddleware` should be after `SessionMiddleware`

2. **Verify URL pattern** includes i18n:
   ```python
   path('i18n/', include('django.conf.urls.i18n')),
   ```

3. **Check form submission:**
   Language switcher forms must use POST method with CSRF token

### Compilation errors

If using Django's `compilemessages` fails (requires gettext):
- Use the included `compile_translations.py` script instead
- This works on all platforms without external dependencies

## Best Practices

1. **Always use translation markers:**
   - In templates: `{% trans "Text" %}`
   - In Python: `_("Text")` or `gettext_lazy`

2. **Keep messages context-aware:**
   - Use descriptive strings
   - Avoid concatenation
   - Consider gender and pluralization

3. **Test both languages:**
   - Switch languages regularly during development
   - Verify all pages display correctly
   - Check for layout issues with longer translations

4. **Maintain consistency:**
   - Use same terms for same concepts
   - Follow Vietnamese grammar rules
   - Keep technical terms in English when appropriate

## Future Enhancements

Potential improvements for multilingual support:

- [ ] More languages (Spanish, French, Mandarin, etc.)
- [ ] User language preference in profile
- [ ] RTL language support (Arabic, Hebrew)
- [ ] Date/time localization
- [ ] Number format localization
- [ ] Pluralization rules
- [ ] Context-specific translations
- [ ] Translation management UI

## Resources

- [Django Internationalization Documentation](https://docs.djangoproject.com/en/4.2/topics/i18n/)
- [Django Translation Documentation](https://docs.djangoproject.com/en/4.2/topics/i18n/translation/)
- [GNU gettext Manual](https://www.gnu.org/software/gettext/manual/)

## Support

For questions about translations or adding new languages, please check:
1. This guide
2. Django i18n documentation
3. Project README.md

---

**EduFlow AI** - Making education accessible in multiple languages!
