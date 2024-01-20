from django.contrib import admin
from .models import *


# from manga_server_django.admin.import_export import CommonImportExportSetting


class InfoImageInline(admin.StackedInline):
    model = InfoImage
    extra = 1


# @admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    inlines = [InfoImageInline]
    list_display = (
        'id',
        'title',
        'user',
        'make_date',
        'update_date',
        'event_flg'
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'user',
        'make_date',
        'update_date',
        'event_flg'
    )
    search_fields = (
        'user',
        'title',
        'detail',
    )
    readonly_fields = (
        'make_date',
        'update_date',
    )


# class RoomTypeInline(admin.StackedInline):
#     model = RoomType
#     extra = 1
# class ServiceInline(admin.StackedInline):
#     model = Service
#     extra = 1
#
# class ServiceDateInline(admin.StackedInline):
#     model = ServiceDate
#     extra = 1
#
# class ServiceTimeInline(admin.StackedInline):
#     model = ServiceTime
#     extra = 1

class InfoAdmin(admin.ModelAdmin):
    inlines = [InfoImageInline]
    list_display = (
        'id',
        'title',
        'user',
        'make_date',
        'update_date',
        'event_flg'
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'user',
        'make_date',
        'update_date',
        'event_flg'
    )
    search_fields = (
        'user',
        'title',
        'detail',
    )
    readonly_fields = (
        'make_date',
        'update_date',
    )


class ServicePriceAdmin(admin.ModelAdmin):
    list_display = (
        'room_type',
        'service',
        'service_date',
        'service_time',
    )
    list_display_links = (
        'room_type',
        'service',
        'service_date',
        'service_time',
    )
    list_filter = (
        'room_type',
        'service',
        'service_date',
        'service_time',
    )
    search_fields = (
        'room_type',
        'service',
        'service_date',
        'service_time',
    )


admin.site.register(Info, InfoAdmin)
admin.site.register(ServicePrice, ServicePriceAdmin)
admin.site.register(RoomType)
admin.site.register(Service)
admin.site.register(ServiceDate)
admin.site.register(ServiceTime)
