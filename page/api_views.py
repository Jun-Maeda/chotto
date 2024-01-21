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
from django.db.models import Q


class InfoListAPIView(APIView):
    def get(self, request):
        try:
            all_info = Info.objects.filter(event_flg=False)
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


class InfoDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            target_info = Info.objects.get(id=pk)
            target_imgs = InfoImage.objects.filter(info=target_info)

            info_json = {
                'id': target_info.id,
                'user': {'id': target_info.user_id,
                         'name': target_info.user.username},
                'title': target_info.title,
                'detail': target_info.detail,
                'images': [{'id': img.id,
                            'img': img.img.path
                            } for img in target_imgs],
                'make_date': target_info.make_date,
                'update_date': target_info.update_date
            }

            return Response(info_json, status=200)
        except:
            return Response("error", status=404)


class EventListAPIView(APIView):
    def get(self, request):
        try:
            all_event = Info.objects.filter(event_flg=True)
            # イベントリストは最初の画像のみ取得して表示
            event_json = [{
                'id': event.id,
                'user': event.user_id,
                'title': event.title,
                'image': InfoImage.objects.filter(info=event)[0].img.path,
                'make_date': event.make_date,
                'update_date': event.update_date
            } for event in all_event]

            return Response(event_json, status=200)
        except:
            return Response("error", status=404)

class ServiceListAPIView(APIView):
    def get(self, request):
        try:
            all_service = Service.objects.all()
            # イベントリストは最初の画像のみ取得して表示
            service_json = [{
                'id': service.id,
                'name': service.name.name,
                'service_date': service.servie_date.name,
                'service_time': service.service_time.name,
                'priority': service.priority
            } for service in all_service]

            return Response(service_json, status=200)
        except:
            return Response("error", status=404)

class ServiceNameListAPIView(APIView):
    def get(self, request):
        try:
            all_service = ServiceName.objects.all().order_by("priority")
            # イベントリストは最初の画像のみ取得して表示
            service_json = [{
                'id': service.id,
                'name': service.name,
                'priority': service.priority
            } for service in all_service]

            return Response(service_json, status=200)
        except:
            return Response("error", status=404)


