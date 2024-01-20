from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from . import views
from . import api_views

urlpatterns = [
	path('info/', api_views.InfoListAPIView.as_view()),
	# path('success/<uuid:pk>', views.SuccessView.as_view(), name='success'),
	# path('CleanUp/<uuid:pk>', views.cleanup, name='cleanup'),
]