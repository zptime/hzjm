# -*- coding: utf-8 -*-

from django.db import models

from utils.const import *
from utils.storage import ImageStorage


class CommonParameter(models.Model):
    key = models.CharField(max_length=50, verbose_name=u'参数关键字')
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u'参数名称')
    value1 = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'参数取值1')
    value2 = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'参数取值2')
    value3 = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'参数取值3')
    is_allow_config = models.BooleanField(default=False, verbose_name=u'是否允许管理员修改')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')

    # 记录系统全局参数： 多少天算new文章， 默认图片地址等等
    class Meta:
        db_table = "common_parameter"
        verbose_name_plural = u"系统参数表"
        verbose_name = u"系统参数表"
        ordering = ['-is_allow_config', 'id']

    def __unicode__(self):
        return self.name


class CommonFileTemp(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'文件名称')
    file = models.FileField(upload_to='temp/files/', storage=ImageStorage(), verbose_name=u'临时文件')
    size = models.CharField(max_length=100, verbose_name=u'文件大小(字节)')
    comments = models.CharField(max_length=255, verbose_name=u'备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')

    class Meta:
        db_table = "common_file_temp"
        verbose_name_plural = u"临时文件表"
        verbose_name = u"临时文件表"

    def __unicode__(self):
        return self.name


class CommonImageTemp(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'图片名称')
    image = models.ImageField(upload_to=TEMP_IMAGE, storage=ImageStorage(), verbose_name=u'临时图片')
    size = models.CharField(max_length=100, verbose_name=u'大小')
    comments = models.CharField(max_length=255, verbose_name=u'备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')

    class Meta:
        db_table = "common_image_temp"
        verbose_name_plural = u"临时图片表"
        verbose_name = u"临时图片表"

    def __unicode__(self):
        return self.name