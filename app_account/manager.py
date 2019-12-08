# -*- coding: utf-8 -*-

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_superuser(self, account, password):
        """
        新增一个数据库管理员用户，通过manager.py的createsuperuser命令行调用
        """
        if not account or not password:
            raise ValueError('UserManager create user parameter error')

        user = self.model(account=account,)

        user.set_password(password)
        user.is_superuser = True
        user.is_db_admin = True
        user.save(using=self._db)

        return user

    def create_user(self, account, password, **kwargs):
        """
        新增一个用户
        """
        pass


    def bulk_create_user(self, **kwargs):
        """
        批量新增用户
        """
        pass