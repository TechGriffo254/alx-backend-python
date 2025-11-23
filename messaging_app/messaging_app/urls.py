"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from chats.auth import register_user, login_user, logout_user


def api_root(request):
    """API root endpoint with available endpoints information."""
    return JsonResponse({
        'message': 'Welcome to Messaging App API',
        'version': '1.0.0',
        'documentation': '/api/',
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
            'Pagination (20 messages/page)',
            'Advanced Filtering',
            'Search Functionality'
        ],
        'status': 'online'
    })


urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    # JWT Authentication endpoints
    path('api/auth/register/', register_user, name='auth_register'),
    path('api/auth/login/', login_user, name='auth_login'),
    path('api/auth/logout/', logout_user, name='auth_logout'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
