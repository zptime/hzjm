# -*- coding=utf-8 -*-

from django.contrib import admin

from app_common.models import CommonImageTemp, CommonFileTemp, CommonParameter


class CommonParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'name', 'is_delete', 'value1', 'is_allow_config']

admin.site.register(CommonParameter, CommonParameterAdmin)


class CommonFileTempAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete', 'file', 'size', 'comments', 'create_time']

admin.site.register(CommonFileTemp, CommonFileTempAdmin)


class CommonImageTempAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_delete', 'image', 'size', 'comments', 'create_time']

admin.site.register(CommonImageTemp, CommonImageTempAdmin)


