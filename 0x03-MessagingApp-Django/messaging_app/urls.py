"""
URL configuration for messaging_app project with Swagger documentation.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from chats.auth import register_user, login_user, logout_user

# Swagger schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title='MessagingApp API',
        default_version='v1',
        description='''
        # MessagingApp API Documentation
        
        A comprehensive REST API for a messaging application with user authentication, 
        conversations, and message management.
        
        ## Features
        - JWT Authentication with token refresh
        - User registration and management
        - Conversation management
        - Message CRUD operations
        - Advanced filtering and pagination
        - Role-based permissions
        - Background email notifications via Celery
        
        ## Authentication
        Most endpoints require authentication. Use the /api/auth/login/ or /api/auth/token/ 
        endpoint to obtain an access token, then include it in the Authorization header:
        
        \\\
        Authorization: Bearer <your-access-token>
        \\\
        
        ## Rate Limiting
        - Maximum 5 POST requests per minute per IP address
        - Time-based access control (9:00 AM - 6:00 PM)
        ''',
        terms_of_service='https://www.messagingapp.com/terms/',
        contact=openapi.Contact(email='support@messagingapp.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

def api_root(request):
    '''API root endpoint with available endpoints information.'''
    return JsonResponse({
        'message': 'Welcome to Messaging App API',
        'version': '1.0.0',
        'documentation': {
            'swagger_ui': '/swagger/',
            'redoc': '/redoc/',
            'swagger_json': '/swagger.json',
        },
        'authentication': {
            'register': '/api/auth/register/',
            'login': '/api/auth/login/',
            'logout': '/api/auth/logout/',
            'token': '/api/auth/token/',
            'token_refresh': '/api/auth/token/refresh/',
            'token_verify': '/api/auth/token/verify/',
        },
        'endpoints': {
            'users': '/api/users/',
            'conversations': '/api/conversations/',
            'messages': '/api/messages/',
            'current_user': '/api/users/me/',
        },
        'features': [
            'JWT Authentication',
            'Role-based Permissions',
            'Pagination (20 items/page)',
            'Advanced Filtering',
            'Search Functionality',
            'Celery Background Tasks',
            'Email Notifications'
        ],
        'status': 'online'
    })

urlpatterns = [
    # API Root
    path('', api_root, name='api_root'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    # JWT Authentication endpoints
    path('api/auth/register/', register_user, name='auth_register'),
    path('api/auth/login/', login_user, name='auth_login'),
    path('api/auth/logout/', logout_user, name='auth_logout'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Swagger Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)\$', 
            schema_view.without_ui(cache_timeout=0), 
            name='schema-json'),
    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
    path('redoc/', 
         schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
