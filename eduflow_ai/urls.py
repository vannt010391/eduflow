"""
URL configuration for eduflow_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf.urls.i18n import i18n_patterns

# Import test view
from test_language_view import test_language_view

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('test-lang/', test_language_view),  # Test view - remove after debugging
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard')),
    path('dashboard/', include('analytics.urls')),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('sessions/', include('study_sessions.urls')),
    path('focus/', include('focus_break.urls')),
    path('emotional/', include('emotional_state.urls')),
    path('diagnostics/', include('diagnostics.urls')),
    prefix_default_language=False,
)
