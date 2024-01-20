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
        'user',
        'title',
        'make_date',
        'update_date',
    )
    list_display_links = (
        'title',
    )
    list_filter = (
        'user',
        'make_date',
        'update_date',
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


admin.site.register(Info, InfoAdmin)
