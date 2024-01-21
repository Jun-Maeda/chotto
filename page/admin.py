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

class MenuImageInline(admin.StackedInline):
    model = MenuImage
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuImageInline]
    list_display = (
        'id',
        'name',
        'type',
    )
    list_display_links = (
        'name',
    )
    list_filter = (
        'name',
        'type',
    )
    search_fields = (
        'name',
        'type',
    )


class ServicePriceAdmin(admin.ModelAdmin):
    list_display = (
        'room_type',
        'service',
        'service_date',
        'price',


    )
    list_display_links = (
        'room_type',
        'service',
    )
    list_filter = (
        'room_type',
        'service',
    )
    search_fields = (
        'room_type',
        'service',
    )


admin.site.register(Info, InfoAdmin)
admin.site.register(ServicePrice, ServicePriceAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(RoomType)
admin.site.register(Service)
admin.site.register(ServiceDate)
admin.site.register(ServiceTime)
admin.site.register(ServiceName)
admin.site.register(MenuType)
