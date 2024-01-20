from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
path('/', include('page.urls')),
path('api/v1/auth/', auth_views.obtain_auth_token, name="auth"),
path('api/v1/page/', include('page.api_urls')),
]
