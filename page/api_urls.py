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
    path('service/', api_views.ServiceListAPIView.as_view()),
    path('room_type/', api_views.RoomTypeListAPIView.as_view()),
    path('room_type/<str:pk>', api_views.RoomTypeDetailAPIView.as_view()),
    path('room/', api_views.RoomListView.as_view()),
    path('room/<str:pk>', api_views.RoomDetailView.as_view()),
    path('home/', api_views.HomeListAPIView.as_view()),
    path('facility/', api_views.FacilityListAPIView.as_view()),
    path('menu/', api_views.MenuList.as_view()),
    # path('service_name/', api_views.ServiceNameListAPIView.as_view()),
    # path('CleanUp/<uuid:pk>', views.cleanup, name='cleanup'),
]
