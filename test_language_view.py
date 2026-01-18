"""
Simple test view to debug language switching.
Add this to your urls.py temporarily:
    path('test-lang/', test_language_view),
"""
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token

@require_http_methods(["GET"])
def test_language_view(request):
    current_lang = get_language()
    cookie_lang = request.COOKIES.get('django_language', 'Not set')
    csrf_token = get_token(request)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Language Test</title>
        <style>
            body {{ font-family: Arial; padding: 20px; }}
            .info {{ background: #e3f2fd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .success {{ background: #c8e6c9; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .error {{ background: #ffcdd2; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>Language Switching Test</h1>

        <div class="info">
            <h2>Current State:</h2>
            <p><strong>Active Language:</strong> {current_lang}</p>
            <p><strong>Cookie Value:</strong> {cookie_lang}</p>
            <p><strong>Request Path:</strong> {request.path}</p>
        </div>

        <div class="success">
            <h2>Test Switching:</h2>

            <h3>Switch to Vietnamese:</h3>
            <form action="/i18n/setlang/" method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="language" value="vi">
                <input type="hidden" name="next" value="/test-lang/">
                <button type="submit" style="padding: 10px 20px; font-size: 16px;">Switch to Vietnamese (vi)</button>
            </form>

            <h3>Switch to English:</h3>
            <form action="/i18n/setlang/" method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="hidden" name="language" value="en">
                <input type="hidden" name="next" value="/test-lang/">
                <button type="submit" style="padding: 10px 20px; font-size: 16px;">Switch to English (en)</button>
            </form>
        </div>

        <div class="info">
            <h2>Debugging Info:</h2>
            <p><strong>All Cookies:</strong> {dict(request.COOKIES)}</p>
            <p><strong>Session Key:</strong> {request.session.session_key if hasattr(request, 'session') else 'No session'}</p>
        </div>

        <div class="error">
            <h2>What Should Happen:</h2>
            <ol>
                <li>Click one of the buttons above</li>
                <li>Page should reload</li>
                <li>"Active Language" should change to the selected language</li>
                <li>"Cookie Value" should update to match</li>
            </ol>
            <p><strong>If it doesn't work:</strong> Check browser console and network tab!</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
