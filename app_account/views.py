# -*- coding: utf-8 -*-

import logging

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST, require_GET

from app_account.models import User
from app_site.models import SiteArticle
from utils.const import *
from utils.err_code import *
from utils.para_check import *
from utils import utils_common
from utils.utils_common import require_roles, respformat

logger = logging.getLogger(__name__)


@require_POST
def manage_user_login(request):
    """
    用户登录
    /api/manage/user/login
    """
    try:
        username = get_parameter(request.POST.get('username'), para_intro='登录账号', valid_check=ACCOUNT)
        password = get_parameter(request.POST.get('password'), para_intro='登录密码', valid_check=PASSWORD)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    user = auth.authenticate(account=username, password=password)

    if not user or user.is_delete or not user.is_active:   # 用户账号密码错误或者未启用
        dict_resp = get_msg(LOGIN_WRONG_ACCOUNT)
    elif user.role not in (DB_USER_ROLE_ADMIN, DB_USER_ROLE_TEACHER):   # 只有门户管理员和教师才可以使用本系统
        dict_resp = get_msg(LOGIN_NO_PRIVILEGES)
    else:
        auth.login(request, user)
        info = {
            'username': user.account,
            'realname': user.name,
            'role': user.role,
            'mobile': user.mobile_phone,
            'intro': user.intro,
        }
        dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": info}

    return utils_common.response(dict_resp)


@login_required
@require_GET
def manage_user_logout(request):
    """
    用户退出
    /api/manage/user/logout
    """
    try:
        auth.logout(request)
        dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
        return utils_common.response(dict_resp)
    except Exception as e:
        logger.error(str(e))
        return utils_common.response({"c": -1, "m": str(e)})


@login_required
@require_GET
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_user_list(request):
    """
    列出所有用户
    /api/manage/user/list
    """
    users_qs = User.objects.filter(is_delete=False).filter(~Q(role=DB_USER_ROLE_OTHER))
    user_list = list()
    for each_user in users_qs:
        user_list.append({
            'id': each_user.id,
            'username': each_user.account,
            'realname': each_user.name,
            'role': str(each_user.role),
            'mobile': each_user.mobile_phone,
            'intro': each_user.intro,
            'is_active': utils_common.bool2str(each_user.is_active)
        })
    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": user_list}
    return utils_common.response(dict_resp)


@login_required
@require_POST
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_user_add(request):
    """
    增加用户
    /api/manage/user/add
    """
    try:
        username = get_parameter(request.POST.get('username'), para_intro='登录账号', valid_check=ACCOUNT)
        password = get_parameter(request.POST.get('password'), para_intro='登录密码', valid_check=PASSWORD)
        realname = get_parameter(request.POST.get('realname'), para_intro='用户名')
        role = get_parameter(request.POST.get('role'), para_intro='角色', allow_null=False,
                    valid_check=CHOICES, choices=(str(DB_USER_ROLE_ADMIN), str(DB_USER_ROLE_TEACHER), str(DB_USER_ROLE_STUDENT), str(DB_USER_ROLE_OTHER)))
        mobile = get_parameter(request.POST.get('mobile'), para_intro='手机号码', allow_null=True, default='')
        intro = get_parameter(request.POST.get('intro'), para_intro='介绍', allow_null=True, default='')
        is_active = get_parameter(request.POST.get('is_active'), para_intro='是否激活', allow_null=True, default=TRUE)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    # 检查用户名是否重复
    if utils_common.is_duplicate_field(username, 'User', 'account'):
        return utils_common.response(get_msg(USER_DUPLICATE_ACCOUNT))

    new_user = User()
    new_user.account = username
    new_user.set_password(password)
    new_user.name = realname
    new_user.role = int(role)
    new_user.mobile_phone = mobile
    new_user.intro = intro
    new_user.is_active = utils_common.str2bool(is_active)
    new_user.is_db_admin = False
    new_user.is_delete = False
    new_user.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@login_required
@require_POST
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_user_edit(request):
    """
    修改用户
    /api/manage/user/edit
    """
    try:
        id = get_parameter(request.POST.get('id'), para_intro='用户ID', valid_check=INTEGER_NONNEGATIVE)
        username = get_parameter(request.POST.get('username'), para_intro='登录账号', valid_check=ACCOUNT)
        realname = get_parameter(request.POST.get('realname'), para_intro='姓名', allow_null=False)
        mobile = get_parameter(request.POST.get('mobile'), para_intro='手机号码', allow_null=True, default='')
        intro = get_parameter(request.POST.get('intro'), para_intro='介绍', allow_null=True, default='')
        is_active = get_parameter(request.POST.get('is_active'), para_intro='是否激活', allow_null=True, default=TRUE)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    this_user = User.objects.filter(is_delete=False, id=id).first()
    if not this_user:
        return utils_common.response(get_msg(USER_NOT_EXIST))

    # 检查用户名是否重复
    if username != this_user.account:
        if utils_common.is_duplicate_field(username, 'User', 'account'):
            return utils_common.response(get_msg(USER_DUPLICATE_ACCOUNT))

    this_user.account = username
    this_user.name = realname
    this_user.mobile_phone = mobile
    this_user.intro = intro
    this_user.is_active = utils_common.str2bool(is_active)
    this_user.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@login_required
@require_POST
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_user_delete(request):
    """
    删除用户
    /api/manage/user/delete
    """
    try:
        id_list = get_parameter(request.POST.get('id_list'), para_intro='用户ID')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    userlist = list()
    for eachid in id_list.split(','):
        this_user = User.objects.filter(is_delete=False, id=eachid).first()
        if not this_user:
            return utils_common.response(get_msg(USER_NOT_EXIST))
        #如果用户发布过文章则不允许删除
        userartcount = SiteArticle.objects.filter(publish_user=this_user, is_delete=False).count()
        if userartcount > 0:
            dict_resp = {"c": USER_HAS_ARTICLE[0], "m": USER_HAS_ARTICLE[1]}
            return utils_common.response(dict_resp)
        #如果列表中包含自己侧跳过
        if this_user.id != request.user.id:
            userlist.append(this_user)

    for eachuser in userlist:
        eachuser.delete()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@login_required
@require_POST
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_user_changepw(request):
    """
    修改自己的账号密码
    /api/manage/user/changepw
    """
    try:
        #id = get_parameter(request.POST.get('id'), para_intro='用户ID', valid_check=INTEGER_NONNEGATIVE)
        oldpw = get_parameter(request.POST.get('oldpw'), para_intro='原密码', valid_check=PASSWORD)
        newpw = get_parameter(request.POST.get('newpw'), para_intro='新密码', valid_check=PASSWORD)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    # 用户不存在
    this_user = User.objects.filter(is_delete=False, id=request.user.id).first()
    if not this_user:
        return utils_common.response(get_msg(USER_NOT_EXIST))

    # 原密码错误
    user = auth.authenticate(account=this_user.account, password=oldpw)
    if not user:
        return utils_common.response(get_msg(USER_OLD_PASSWORD_WRONG))

    this_user.set_password(newpw)
    this_user.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@login_required
@require_POST
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_user_resetpw(request):
    """
    重置某一个用户的账号密码
    /api/manage/user/resetpw
    """
    try:
        id = get_parameter(request.POST.get('id'), para_intro='用户ID', valid_check=INTEGER_NONNEGATIVE)
        newpw = get_parameter(request.POST.get('newpw'), para_intro='新密码', valid_check=PASSWORD)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    # 用户不存在
    this_user = User.objects.filter(is_delete=False, id=id).first()
    if not this_user:
        return utils_common.response(get_msg(USER_NOT_EXIST))

    this_user.set_password(newpw)
    this_user.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)