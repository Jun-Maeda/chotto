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


# サービス取得
def get_service(name, service_all):
    try:
        service_filter = service_all.filter(name=name).order_by('priority')
        filter_json = [
            {'id': service.id,
             'service_date': service.service_date.name,
             'service_time': service.service_time.name,
             }
            for service in service_filter
        ]
        return filter_json
    except:
        return []


class ServiceListAPIView(APIView):
    def get(self, request):
        try:
            all_service = Service.objects.all()
            all_service_name = ServiceName.objects.all().order_by("priority")
            # イベントリストは最初の画像のみ取得して表示
            service_json = [{
                'id': service_name.id,
                'name': service_name.name,
                'service': get_service(service_name, all_service),
                'priority': service_name.priority
            } for service_name in all_service_name]

            return Response(service_json, status=200)
        except:
            return Response("error", status=404)


def get_room(type, room_all):
    try:
        room_filter = room_all.filter(type=type).order_by('name')
        filter_json = [{
            'id': room.id,
            'name': room.name
        }
            for room in room_filter
        ]
        return filter_json
    except:
        return []


class RoomTypeListAPIView(APIView):
    def get(self, request):
        try:
            room_types = RoomType.objects.all()
            room_all = Room.objects.all()
            # タイプでフィルターがある場合名前でフィルター
            type_filter = self.request.GET.get('type')
            if type_filter:
                room_types = room_types.filter(id=type_filter)

            type_json = [{
                'id': type.id,
                'name': type.name,
                'rooms': get_room(type, room_all),
            } for type in room_types]

            return Response(type_json, status=200)
        except:
            return Response("error", status=404)


def get_service_prices(service_name, price_filter):
    try:
        price_filter = price_filter.filter(service=service_name).order_by('priority')
        filter_json = [{
            'id': price.id,
            'serice_date': price.service_date.name,
            'price': price.price,
            'priority': price.priority
        }
            for price in price_filter
        ]
        return filter_json
    except:
        return []


def get_service_details(service_name, service_all):
    try:
        service_filter = service_all.filter(name=service_name).order_by('priority')
        filter_json = [{
            'id': service.id,
            'serice_date': service.service_date.name,
            'service_time': service.service_time.name,
            'priority': service.priority
        }
            for service in service_filter
        ]
        return filter_json
    except:
        return []


def get_price(type, price_all):
    try:
        price_filter = price_all.filter(room_type=type)
        all_service_name = ServiceName.objects.all().order_by("priority")
        service_all = Service.objects.all()
        filter_json = [{
            'id': service_name.id,
            'name': service_name.name,
            'detail': get_service_details(service_name, service_all),
            'prices': get_service_prices(service_name, price_filter)
        }
            for service_name in all_service_name
        ]
        return filter_json
    except:
        return []


class RoomTypeDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            room_type = RoomType.objects.get(id=pk)
            room_all = Room.objects.all()
            price_all = ServicePrice.objects.all()

            type_json = {
                'id': room_type.id,
                'name': room_type.name,
                'rooms': get_room(room_type, room_all),
                'services': get_price(room_type, price_all)
            }

            return Response(type_json, status=200)
        except:
            return Response("error", status=404)

# class ServiceNameListAPIView(APIView):
#     def get(self, request):
#         try:
#             all_service = ServiceName.objects.all().order_by("priority")
#             # イベントリストは最初の画像のみ取得して表示
#             service_json = [{
#                 'id': service.id,
#                 'name': service.name,
#                 'priority': service.priority
#             } for service in all_service]
#
#             return Response(service_json, status=200)
#         except:
#             return Response("error", status=404)
