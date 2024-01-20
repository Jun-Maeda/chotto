from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from . import views
from . import api_views

urlpatterns = [
    path('info/', api_views.InfoListAPIView.as_view()),
    path('event/', api_views.EventListAPIView.as_view()),
    path('info/<str:pk>', api_views.InfoDetailAPIView.as_view()),
    # path('CleanUp/<uuid:pk>', views.cleanup, name='cleanup'),
]
