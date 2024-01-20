from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
import json
import requests
from django.contrib.auth.mixins import LoginRequiredMixin


class InfoListAPIView(APIView):
    def get(self, request):
        try:
            all_info = Info.objects.all()
            info_json = [{
                'id': info.id,
                'user': info.user_id,
                'title': info.title,
                'make_date': info.make_date,
                'update_date': info.update_date
            } for info in all_info]

            return Response(info_json, status=200)
        except:
            return Response("error", status=404)
