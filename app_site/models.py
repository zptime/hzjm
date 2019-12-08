# -*- coding: utf-8 -*-

from datetime import datetime
from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model
from django.db import models

from upload_resumable.models import FileObj
from utils.const import *
from utils.storage import ImageStorage, Storage

from app_account.models import User


def dir_article_cover(instance, filename):
    return ARTICLE_COVER % (datetime.now().strftime('%Y%m'), filename)


def dir_expert_image(instance, filename):
    return EXPERT_IMAGE % filename


def dir_article_image():
    return ARTICLE_IMAGE % datetime.now().strftime('%Y%m')


def dir_article_file():
    return ARTICLE_FILE % datetime.now().strftime('%Y%m')


def dir_article_video():
    return ARTICLE_VIDEO % datetime.now().strftime('%Y%m')


def get_sentinel_user():
    return get_user_model().objects.get_or_create(
        account='deleted_user', name=u'佚名', is_db_admin=False, role=DB_USER_ROLE_OTHER)[0]


class SiteExpert(models.Model):
    expert_name = models.CharField(max_length=30, verbose_name=u'姓名')
    image_url = models.ImageField(upload_to=dir_expert_image, storage=ImageStorage(), blank=True, null=True, verbose_name=u'用户头像')
    article_num = models.IntegerField(default=0, verbose_name=u'文章数量')
    expert_intro = models.CharField(max_length=500, blank=True, null=True, default='', verbose_name=u'专家简介')
    sort_order = models.IntegerField(default=100, verbose_name=u'排序')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')

    class Meta:
        db_table = "site_expert"
        verbose_name_plural = verbose_name = u'门户专家'
        ordering = ['sort_order']

    def __unicode__(self):
        return self.expert_name


class SiteArticle(models.Model):
    title = models.CharField(max_length=300, verbose_name=u'标题')
    subtitle = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'二级标题')
    # category = models.ForeignKey(SiteCategory, verbose_name=u'对应栏目')
    publish_user = models.ForeignKey(User, related_name='publish_user', verbose_name=u'发布用户', on_delete=models.SET(get_sentinel_user))
    author = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=u'作者')
    keyword = models.CharField(max_length=500, blank=True, null=True, default='', verbose_name=u'关键字(多个用逗号分割)') # 暂不使用
    image = models.ImageField(upload_to=dir_article_cover, storage=ImageStorage(), blank=True, null=True, verbose_name=u'封面')
    # image = models.CharField(max_length=100, blank=True, null=True, default='', verbose_name=u'封面')
    intro = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'摘要')
    click = models.IntegerField(default=0, verbose_name=u'点击数量')
    content = UEditorField(u'内容', blank=True, default='', toolbars='full',
                           imagePath=dir_article_image(),
                           filePath=dir_article_file())
    publish_time = models.DateTimeField(blank=True, null=True, verbose_name=u'发布时间')  # 可手动选择，可精确到秒，默认是创建时间，如果为空则传给前台创建时间
    admit_status = models.IntegerField(
        default=0, choices=((DB_ARTICLE_ADMIT_STATE_PEND, u'待审核'), (DB_ARTICLE_ADMIT_STATE_PASS, u'通过审核'), (DB_ARTICLE_ADMIT_STATE_FAIL, u'未通过审核')), verbose_name=u'审核状态')
    admit_user = models.ForeignKey(User, related_name='admit_user', blank=True, null=True, verbose_name=u'审核人', on_delete=models.SET(get_sentinel_user))
    admit_time = models.DateTimeField(blank=True, null=True, verbose_name=u'审核通过时间')
    is_top = models.BooleanField(default=False, verbose_name=u'是否置顶')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')
    expert = models.ForeignKey(SiteExpert, related_name='sitearticleexpert', verbose_name=u'专家', blank=True, null=True)
    video = models.ForeignKey(FileObj, related_name='sitearticlefileobj', verbose_name=u'视频', blank=True, null=True)

    class Meta:
        db_table = "site_article"
        verbose_name_plural = verbose_name = u'门户文章'
        ordering = ['-is_top', '-publish_time']

    def __unicode__(self):
        return self.title

