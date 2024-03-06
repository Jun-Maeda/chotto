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


def target_img(target_info):
    target_imgs = InfoImage.objects.filter(info=target_info)
    return target_imgs


class InfoListAPIView(APIView):
    def get(self, request):
        try:
            all_info = Info.objects.filter(event_flg=False).order_by('-update_date')
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

            info_json = {
                'id': target_info.id,
                'user': {'id': target_info.user_id,
                         'name': target_info.user.username},
                'title': target_info.title,
                'detail': target_info.detail,
                'images': [{'id': img.id,
                            'img': img.img.path
                            } for img in target_img(target_info)],
                'make_date': target_info.make_date,
                'update_date': target_info.update_date
            }

            return Response(info_json, status=200)
        except:
            return Response("error", status=404)


class EventListAPIView(APIView):
    def get(self, request):
        try:
            all_event = Info.objects.filter(event_flg=True).order_by('-update_date')
            # イベントリストは最初の画像のみ取得して表示
            event_json = [{
                'id': event.id,
                'user': event.user_id,
                'title': event.title,
                'make_date': event.make_date,
                'update_date': event.update_date,
                'images': {'id': target_img(event)[0].id,
                           'img': target_img(event)[0].img.path
                           },
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


class HomeListAPIView(APIView):
    def get(self, request):
        try:
            all_info = Info.objects.filter(event_flg=False).order_by('-update_date')[0:3]
            info_json = [{
                'id': info.id,
                'user': info.user_id,
                'title': info.title,
                'make_date': info.make_date,
                'update_date': info.update_date
            } for info in all_info]

            all_event = Info.objects.filter(event_flg=True).order_by('-update_date')[0:3]
            # イベントリストは最初の画像のみ取得して表示
            event_json = [{
                'id': event.id,
                'user': event.user_id,
                'title': event.title,
                'make_date': event.make_date,
                'update_date': event.update_date,
                'images': {'id': target_img(event)[0].id,
                           'img': target_img(event)[0].img.path
                           },
            } for event in all_event]

            result = {
                'infos': info_json,
                'events': event_json
            }

            return Response(result, status=200)
        except:
            return Response("error", status=404)


# 設備情報から設備に対応する部屋一覧を取得する
def facility_rooms(facility_object):
    limited_room = facility_object.limited_room.all()
    result = [{
        'id': room.id,
        'name': room.name
    } for room in limited_room]
    return result


# 設備ページ
class FacilityListAPIView(APIView):
    def get(self, request):
        try:
            facility_all = Facility.objects.all()
            room_all = Room.objects.all()

            # 通常設備
            normal_facility_all = facility_all.filter(vip_flg=False, limited_room=None)
            normal_lists = [{
                'id': normal.id,
                'name': normal.name,
            } for normal in normal_facility_all]
            normal_imgs = []
            for normal in normal_facility_all:
                if normal.img.name is not "":
                    normal_imgs.append(normal.img.path)

            normal_result = {
                'facilities': normal_lists,
                'imgs': normal_imgs
            }

            # VIP設備
            vip_facility_all = facility_all.filter(vip_flg=True, limited_room=None)
            vip_lists = [{
                'id': vip.id,
                'name': vip.name,
            } for vip in vip_facility_all]
            vip_imgs = []
            for vip in vip_facility_all:
                if vip.img.name is not "":
                    vip_imgs.append(vip.img.path)

            vip_rooms = Room.objects.filter(type__name='VIP')
            vip_room_lists = [{
                'id': v.id,
                'name': v.name
            } for v in vip_rooms]

            vip_result = {
                'facilities': vip_lists,
                'imgs': vip_imgs,
                'rooms': vip_room_lists
            }

            # 限定設備
            limited_facility_all = facility_all.exclude(limited_room__exact=None)
            limited_result = []
            for limited in limited_facility_all:
                img_path = ''
                if limited.img.name is not "":
                    img_path = limited.img.path
                limited = {
                    'id': limited.id,
                    'name': limited.name,
                    'img': img_path,
                    'rooms': facility_rooms(limited)
                }
                limited_result.append(limited)

            facility_result = {
                'normal': normal_result,
                'vip': vip_result,
                'limited_facilities': limited_result
            }

            return Response(facility_result, status=200)
        except Exception as e:
            return Response(e, status=404)


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


class RoomDetailView(APIView):
    def get(self, request, pk):
        try:
            room = Room.objects.get(id=pk)
            images = [r.img for r in room.img.all()]
            facility_all = Facility.objects.all()
            limited_facilities = []
            vip_facilities = []

            limited_facility_all = facility_all.filter(limited_room=room)
            if len(limited_facility_all) > 0:
                limited_facilities = [
                    {'id': limited.id, 'name': limited.name} for limited in limited_facility_all
                ]
            if room.type_id == 2:
                vip_facility = facility_all.filter(vip_flg=True)
                vip_facilities = [
                    {'id': vip.id, 'name': vip.name} for vip in vip_facility
                ]

            normal_facility = facility_all.filter(vip_flg=False, limited_room=None)
            normal_result = [{'id': normal.id, 'name': normal.name} for normal in normal_facility]
            room_detail = {
                'id': room.id,
                'name': room.name,
                'type': {'id': room.type.id, 'name': room.type.name},
                'images': images,
                'facilities': {
                    'limited': limited_facilities,
                    'vip': vip_facilities,
                    'normal': normal_result
                }
            }
            return Response(room_detail, status=200)
        except Exception as e:
            return Response(e, status=404)


def get_menu_category(menu_type):
    menu_category_all = MenuCategory.objects.all()
    target_cat = menu_category_all.filter(type=menu_type)
    result = [
        {
            'id': category.id,
            'name': category.name,
            'menus': get_menu(category)
        }for category in target_cat
    ]
    return result

def get_image(menu):
    all_images = MenuImage.objects.all()
    target_image = all_images.filter(menu=menu)
    result = [
        {
            'id': image.id,
            'image': image.img.path
        }for image in target_image
    ]
    return result

def get_menu(menu_category):
    menu_all = Menu.objects.all()
    target_menu = menu_all.filter(category=menu_category)
    result = [
        {
            'id': menu.id,
            'name': menu.name,
            'price': menu.price,
            'member_price': menu.member_price,
            'welcome_flg': menu.welcome_flg,
            'images': get_image(menu)
        }for menu in target_menu
    ]
    return result

def get_welcome():
    menu_all = Menu.objects.all()
    target_menu = menu_all.filter(welcome_flg=True)
    result = [
        {
            'id': menu.id,
            'name': menu.name,
            'price': menu.price,
            'member_price': menu.member_price,
            'welcome_flg': menu.welcome_flg,
            'images': get_image(menu)
        } for menu in target_menu
    ]
    return result


class MenuList(APIView):
    def get(self, request):
        try:
            menu_type_all = MenuType.objects.all()
            menu_all = [
                {
                    'id': type.id,
                    'name': type.name,
                    'categories': get_menu_category(type),
                } for type in menu_type_all
            ]
            menu_result = {
                'menu': menu_all,
                'welcome': get_welcome()
            }
            return Response(menu_result, status=200)
        except Exception as e:
            return Response(e, status=404)
