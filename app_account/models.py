# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from app_account import manager
from utils.const import *


class User(AbstractBaseUser, PermissionsMixin):
    """
        用户表
        备注： AbstractBaseUser已经包含了password和lastlogin
    """
    account = models.CharField(max_length=30, unique=True, db_index=True, verbose_name=u'账号')
    name = models.CharField(max_length=30, verbose_name=u'姓名')
    is_db_admin = models.BooleanField(default=False, verbose_name=u'是否是后台数据库管理员')  # 限定一个
    role = models.IntegerField(
        default=DB_USER_ROLE_TEACHER, choices=(
        (DB_USER_ROLE_ADMIN, u'管理员'), (DB_USER_ROLE_TEACHER, u'老师'), (DB_USER_ROLE_STUDENT, u'学生'), (DB_USER_ROLE_OTHER, u'其它')),
        verbose_name=u'用户角色')
    mobile_phone = models.CharField(max_length=30, blank=True, null=True, verbose_name=u'手机号')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    intro = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'介绍')
    is_active = models.BooleanField(default=True, verbose_name=u'是否有效')
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')

    objects = manager.UserManager()

    USERNAME_FIELD = 'account'

    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name_plural = u"用户表"
        ordering = ['-create_time']
        verbose_name = u"用户表"

    def __unicode__(self):
        return self.account

    def get_full_name(self):
        return self.account

    def get_short_name(self):
        return self.account

    @property
    def is_staff(self):
        return self.is_db_admin

