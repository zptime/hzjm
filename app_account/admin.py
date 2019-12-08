# -*- coding: utf-8 -*-

from django.contrib import admin

from app_account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'name', 'role', 'mobile_phone', 'is_active', 'is_delete', 'update_time']
    list_filter = ['role']  # 过滤字段
    readonly_fields = ['is_superuser', 'is_db_admin']  # 只读字段
    # search_fields = ['account', 'name']

    def save_model(self, request, obj, form, change):
        if 'pbkdf2_sha256' not in obj.password:
            obj.set_password(obj.password)
        obj.save()

admin.site.register(User, UserAdmin)