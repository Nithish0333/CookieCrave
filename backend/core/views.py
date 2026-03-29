import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@require_GET
@csrf_exempt
def index_view(request):
    """
    Root view for Fast2SMS website verification
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="fast2sms" content="HqUblMmQXuNjycd18enMyJJhMSmO2A3k">
        <title>CookieCrave Backend</title>
    </head>
    <body>
        <h1>CookieCrave Backend is running</h1>
        <p>This page is used for Fast2SMS website verification.</p>
    </body>
    </html>
    """
    return HttpResponse(html_content)


@require_GET
@csrf_exempt
def serve_media_with_cors(request, file_path):
    """
    Serve media files with proper CORS headers
    """
    # Security check - prevent directory traversal
    if '..' in file_path or file_path.startswith('/'):
        raise Http404("File not found")
    
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise Http404("File not found")
    
    try:
        with open(full_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
        
        # Add CORS headers
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        
        # Cache headers
        response['Cache-Control'] = 'public, max-age=3600'
        
        return response
    except Exception as e:
        raise Http404("File not found")
