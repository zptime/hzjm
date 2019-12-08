# -*- coding: utf-8 -*-

from django.contrib import admin

from app_site.models import SiteArticle


# class SiteComponentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'key', 'name', 'is_delete', 'intro', 'link', 'image']
#
# admin.site.register(SiteComponent, SiteComponentAdmin)
#
#
# class SiteChannelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'key', 'name', 'is_delete', 'sort', 'is_navi_show', 'is_active', 'link']
#
# admin.site.register(SiteChannel, SiteChannelAdmin)
#
#
# class SiteCategoryTypeAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'is_delete', 'page_list', 'page_content', 'page_draft', 'page_preview']
#
# admin.site.register(SiteCategoryType, SiteCategoryTypeAdmin)
#
#
# class SiteCategoryAdmin(admin.ModelAdmin):
#     list_display = ['id', 'key', 'name', 'is_delete', 'channel', 'sort', 'type', 'is_default', 'is_active', 'is_support_direct', 'link']
#
# admin.site.register(SiteCategory, SiteCategoryAdmin)


class SiteArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_delete', 'publish_user', 'admit_status', 'is_top', 'publish_time', 'click']
    readonly_fields = ['click']
admin.site.register(SiteArticle, SiteArticleAdmin)

