"""
URL configuration for simpleaccountstorage project.

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
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static
from django.views.generic import TemplateView

from .views import CsrfTokenView


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # CSRF token endpoint
    path('api/csrf/', CsrfTokenView.as_view()),

    # Authentication endpoints
    path('api/v1/auth/', include('rest_registration.api.urls')),
    path('api/v1/auth/', include('authentication.urls')),

    # Accounts CRUD APIs
    path('api/v1/accounts/', include('accountstorage.urls')),
]

# If DEBUG is True, add also the authentication endpoints provided
# by Django REST Framework
if settings.DEBUG:
    urlpatterns += [
        path('drf-auth/', include('rest_framework.urls')),
    ]

# If DEBUG is False, serve also the SPA static files.
#
# This should be made directly by Nginx (or another web server, and that's the best practice)
# but, just to be more comfortable, I'll do that using Django.
#
# You can just configure your webserver to serve the STATIC_ROOT directly.
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^(?P<path>assets\/.*)$', serve_static, {'insecure': True}),
        re_path(r'^(?P<path>images\/.*)$', serve_static, {'insecure': True}),
        re_path('^(?P<path>.*)$', TemplateView.as_view(template_name='index.html')),
    ]
