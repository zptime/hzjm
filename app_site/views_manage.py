# -*- coding: utf-8 -*-
import datetime
import logging
import os
import shutil
from urllib import unquote

import sys
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

import services
from app_site.models import *
from hzjm import settings
from hzjm.settings import BASE_DIR, CHUNKED_UPLOAD_PATH
from utils import utils_common
from utils.const import *
from utils.err_code import *
from utils.net_helper import response_exception
from utils.para_check import *
from utils.utils_common import require_roles, respformat

logger = logging.getLogger(__name__)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN, ))
# def manage_channel_list(request):
#     """
#         获取所有频道和栏目
#     """
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.load_hierarchical_channels(only_show_active=False)}
#     return utils.response(dict_resp)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_TEACHER,))
# def manage_channel_avai_list(request):
#     """
#         老师登录时获取可用频道和栏目
#     """
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.load_hierarchical_channels(user=request.user)}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_level1_edit(request):
#     """
#         修改一个频道
#     """
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='频道ID编号', valid_check=INTEGER_NONNEGATIVE)
#         key = get_parameter(request.POST.get('key'), para_intro='频道关键字', allow_null=True)
#         name = get_parameter(request.POST.get('name'), para_intro='频道名称')
#         link = get_parameter(request.POST.get('link'), para_intro='频道链接地址', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接'
#                                          , allow_null=True, default='1', valid_check=CHOICES, choices=(TRUE, FALSE))
#         is_active = get_parameter(request.POST.get('is_active'), para_intro='是否有效'
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查频道是否存在
#     try:
#         chan = SiteChannel.objects.get(is_delete=False, id=id)
#     except (ObjectDoesNotExist, MultipleObjectsReturned), e:
#         logger.exception(e)
#         return utils.response(get_msg(CHANNEL_INVALID))
#
#     # 如果修改了关键字，则判断关键字是否与现有的重复
#     if key != chan.key:
#         occupied_key_list = services.load_occupied_column_key()
#         if key in occupied_key_list:
#             return utils.response(
#                 {'c': CHANNEL_OCCUPIED_KEY[0], 'm': CHANNEL_OCCUPIED_KEY[1] % ' | '.join(occupied_key_list)})
#
#     if key:
#         chan.key = key
#     chan.name = name
#     if link:
#         chan.link = link
#     if is_link_out_open:
#         chan.is_link_out_open = utils.str2bool(is_link_out_open)
#     if is_active:
#         chan.is_active = utils.str2bool(is_active)
#     chan.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
# def manage_channel_level1_list(request):
#     """
#         获取所有频道
#     """
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.load_channels()}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_level2_delete(request):
#     """
#         删除一个二级栏目
#     """
#     try:
#         id_list = get_parameter(request.POST.get('id_list'), para_intro='栏目ID编号列表')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     #检查是否能够删除
#     level2_list = list()
#     for eachid in id_list.split(','):
#         try:
#             cate = SiteCategory.objects.get(is_delete=False, id=eachid)
#         except (ObjectDoesNotExist, MultipleObjectsReturned), e:
#             logger.exception(e)
#             return utils.response(get_msg(CHANNEL_CATEGORY_INVALID))
#
#         # 栏目下有文章不可删除
#         if SiteArticle.objects.filter(is_delete=False, category=cate).exists():
#             return utils.response(get_msg(CHANNEL_CATEGORY_CANNOT_DELETE))
#
#         level2_list.append(cate)
#
#     #逐个删除栏目
#     for eachcate in level2_list:
#         eachcate.is_delete = True
#         eachcate.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_level2_edit(request):
#     """
#         修改一个二级栏目
#     """
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='栏目ID编号', valid_check=INTEGER_NONNEGATIVE)
#         channel_id = get_parameter(request.POST.get('channel_id'), para_intro='所在频道的ID编号', valid_check=INTEGER_NONNEGATIVE)
#         key = get_parameter(request.POST.get('key'), para_intro='栏目关键字')
#         name = get_parameter(request.POST.get('name'), para_intro='栏目名称')
#         link = get_parameter(request.POST.get('link'), para_intro='栏目链接地址', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接'
#                                          , allow_null=True, default='1', valid_check=CHOICES, choices=(TRUE, FALSE))
#         type_id = get_parameter(request.POST.get('type_id'), para_intro='栏目类型ID编号', valid_check=INTEGER_NONNEGATIVE)
#         sort = get_parameter(request.POST.get('sort'), para_intro='排序'
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default=CHANNEL_SORT_DEFAULT)
#         is_active = get_parameter(request.POST.get('is_active'), para_intro='是否有效'
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#         is_navi_show = get_parameter(request.POST.get('is_navi_show'), para_intro='是否在导航栏显示'
#                             , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#         is_default = get_parameter(request.POST.get('is_default'), para_intro='是否是频道下的默认栏目'
#                                    , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='0')
#         is_support_direct = get_parameter(request.POST.get('is_support_direct'), para_intro='是否支持单文直达'
#                                           , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='0')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查所在栏目是否存在
#     try:
#         cate = SiteCategory.objects.get(is_delete=False, id=id)
#     except (ObjectDoesNotExist, MultipleObjectsReturned), e:
#         logger.exception(e)
#         return utils.response(get_msg(CHANNEL_CATEGORY_INVALID))
#
#     # 如果修改了关键字，则判断关键字是否与现有的重复
#     if key != cate.key:
#         occupied_key_list = services.load_occupied_column_key()
#         if key in occupied_key_list:
#             return utils.response(
#                 {'c': CHANNEL_OCCUPIED_KEY[0], 'm': CHANNEL_OCCUPIED_KEY[1] % ' | '.join(occupied_key_list)})
#
#     # 如果栏目下面有文章，则不允许修改栏目类型
#     if cate.type.id != int(type_id):
#         if SiteArticle.objects.filter(is_delete=False, category=cate).exists():
#             return utils.response(get_msg(CHANNEL_CATEGORY_TYPE_CANNOT_CHANGE))
#
#     # 检查所在栏目类型是否存在
#     cate_type_qs = SiteCategoryType.objects.filter(is_delete=False, id=type_id)
#     if not cate_type_qs.exists():
#         return utils.response(get_msg(CHANNEL_CATEGORY_TYPE_INVALID))
#
#     # 检查所在频道是否存在
#     channel_qs = SiteChannel.objects.filter(is_delete=False, id=channel_id)
#     if not channel_qs.exists():
#         return utils.response(get_msg(CHANNEL_INVALID))
#
#     # 检查允许直达和栏目类型设定是否冲突
#     if not cate_type_qs.first().is_allow_direct:
#         if utils.str2bool(is_support_direct):
#             return utils.response(get_msg(CHANNEL_CATEGORY_DIRECT_CONFLICT))
#
#     cate.key = key
#     cate.name = name
#     cate.link = link
#     cate.is_link_out_open = utils.str2bool(is_link_out_open)
#     cate.type = cate_type_qs.first()
#     cate.channel = channel_qs.first()
#     cate.is_default = utils.str2bool(is_default)
#     cate.is_support_direct = utils.str2bool(is_support_direct)
#     cate.is_active = utils.str2bool(is_active)
#     cate.is_navi_show = utils.str2bool(is_navi_show)
#     cate.sort = int(sort)
#     cate.is_delete = False
#     cate.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_level2_add(request):
#     """
#         增加一个二级栏目
#     """
#     try:
#         channel_id = get_parameter(request.POST.get('channel_id'), para_intro='所在频道的ID编号', valid_check=INTEGER_NONNEGATIVE)
#         key = get_parameter(request.POST.get('key'), para_intro='栏目关键字')
#         name = get_parameter(request.POST.get('name'), para_intro='栏目名称')
#         link = get_parameter(request.POST.get('link'), para_intro='栏目链接地址', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接'
#                                          , allow_null=True, default='1', valid_check=CHOICES, choices=(TRUE, FALSE))
#         type_id = get_parameter(request.POST.get('type_id'), para_intro='栏目类型ID编号', valid_check=INTEGER_NONNEGATIVE)
#         sort = get_parameter(request.POST.get('sort'), para_intro='排序'
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default=CHANNEL_SORT_DEFAULT)
#         is_active = get_parameter(request.POST.get('is_active'), para_intro='是否有效'
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#         is_navi_show = get_parameter(request.POST.get('is_navi_show'), para_intro='是否在导航栏显示'
#                             , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#         is_default = get_parameter(request.POST.get('is_default'), para_intro='是否是频道下的默认栏目'
#                                    , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='0')
#         is_support_direct = get_parameter(request.POST.get('is_support_direct'), para_intro='是否支持单文直达'
#                                           , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='0')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查所在栏目类型是否存在
#     cate_type_qs = SiteCategoryType.objects.filter(is_delete=False, id=type_id)
#     if not cate_type_qs.exists():
#         return utils.response(get_msg(CHANNEL_CATEGORY_TYPE_INVALID))
#     cate_type = cate_type_qs.first()
#
#     # 检查所在频道是否存在
#     channel_qs = SiteChannel.objects.filter(is_delete=False, id=channel_id)
#     if not channel_qs.exists():
#         return utils.response(get_msg(CHANNEL_INVALID))
#
#     # 检查关键字是否全局重复
#     occupied_key_list = services.load_occupied_column_key()
#     if key in occupied_key_list:
#         return utils.response({'c': CHANNEL_OCCUPIED_KEY[0], 'm': CHANNEL_OCCUPIED_KEY[1] % ' | '.join(occupied_key_list)} )
#
#     # 检查允许直达和栏目类型设定是否冲突
#     if not cate_type.is_allow_direct:
#         if utils.str2bool(is_support_direct):
#             return utils.response(get_msg(CHANNEL_CATEGORY_DIRECT_CONFLICT))
#
#     new_cate = SiteCategory()
#     new_cate.key = key
#     new_cate.name = name
#     new_cate.link = link
#     new_cate.is_link_out_open = utils.str2bool(is_link_out_open)
#     new_cate.type = cate_type
#     new_cate.channel = channel_qs.first()
#     new_cate.is_default = utils.str2bool(is_default)
#     new_cate.is_support_direct = utils.str2bool(is_support_direct)
#     new_cate.is_active = utils.str2bool(is_active)
#     new_cate.is_navi_show = utils.str2bool(is_navi_show)
#     new_cate.sort = int(sort)
#     new_cate.is_delete = False
#     new_cate.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_type_list(request):
#     push_channels = services.load_category_types()
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": push_channels}
#     return utils.response(dict_resp)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_push_list(request):
#     """
#         获取所有推送栏目（包含未启用的）
#     """
#     push_channels = services.load_push_channels()
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": push_channels}
#     return utils.response(dict_resp)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
# def manage_channel_push_avai_list(request):
#     """
#         获取可发文的推送栏目（排除了未启用的）
#     """
#     push_channels = services.load_push_channels(only_show_active=True)
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": push_channels}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_push_delete(request):
#     try:
#         id_list = get_parameter(request.POST.get('id_list'), para_intro='推送频道ID编号列表')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查推送频道的ID是否合法
#     site_push_channel_dellist = list()
#     for eachid in id_list.split(','):
#         site_push_channel_qs = SitePushChannel.objects.filter(is_delete=False, id=eachid)
#         if not site_push_channel_qs.exists():
#             utils.response(get_msg(CHANNEL_PUSH_INVALID))
#
#         this_push_channel = site_push_channel_qs.first()
#
#         # 如果推送频道有文章，则不允许删除
#         if SitePushArticle.objects.filter(push_channel = this_push_channel).exists():
#             return utils.response(get_msg(CHANNEL_CATEGORY_CANNOT_DELETE))
#         site_push_channel_dellist.append(this_push_channel)
#
#     for eachdel in site_push_channel_dellist:
#         eachdel.is_delete = True
#         eachdel.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_push_edit(request):
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='推送频道ID编号', valid_check=INTEGER_NONNEGATIVE)
#         key = get_parameter(request.POST.get('key'), para_intro='推送频道关键字')
#         name = get_parameter(request.POST.get('name'), para_intro='推送频道名称')
#         is_active = \
#             get_parameter(request.POST.get('is_active'), para_intro='是否有效', valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查推送频道的ID是否合法
#     site_push_channel_qs = SitePushChannel.objects.filter(is_delete=False, id=id)
#     if not site_push_channel_qs.exists():
#         utils.response(get_msg(CHANNEL_PUSH_INVALID))
#
#     this_push_channel = site_push_channel_qs.first()
#
#     # 检查关键字是否全局重复
#     if key != this_push_channel.key:
#         occupied_key_list = services.load_occupied_column_key()
#         if key in occupied_key_list:
#             return utils.response(
#                 {'c': CHANNEL_OCCUPIED_KEY[0], 'm': CHANNEL_OCCUPIED_KEY[1] % ' | '.join(occupied_key_list)})
#
#     this_push_channel.name = name
#     this_push_channel.key = key
#     this_push_channel.is_active = utils.str2bool(is_active)
#     this_push_channel.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_push_add(request):
#     try:
#         key = get_parameter(request.POST.get('key'), para_intro='推送频道关键字')
#         name = get_parameter(request.POST.get('name'), para_intro='推送频道名称')
#         is_active = \
#             get_parameter(request.POST.get('is_active'), para_intro='是否有效', valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查关键字是否全局重复
#     occupied_key_list = services.load_occupied_column_key()
#     if key in occupied_key_list:
#         return utils.response(
#             {'c': CHANNEL_OCCUPIED_KEY[0], 'm': CHANNEL_OCCUPIED_KEY[1] % ' | '.join(occupied_key_list)})
#
#     new_push_channel = SitePushChannel()
#     new_push_channel.name = name
#     new_push_channel.key = key
#     new_push_channel.is_active = is_active
#     new_push_channel.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
# def manage_channel_level2_list(request):
#     """
#         获取某一个频道的所有栏目（包含未启用的）
#     """
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='频道ID', valid_check=INTEGER_NONNEGATIVE)
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     channel_qs = SiteChannel.objects.filter(is_delete=False, pk=id)
#     if not channel_qs.exists():
#         return utils.response(get_msg(CHANNEL_INVALID))
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.load_categorys(channel_qs.first())}
#     return utils.response(dict_resp)


@require_POST
def manage_article_list(request):
    """
        获取所有文章,管理员可以看到所有的文章，老师只能看到自己发布的文章
        /api/manage/article/list
    """
    try:
        title_key = get_parameter(request.POST.get('title_key'), para_intro='标题关键字'
                                  , allow_null=True, default='')
        expert_id = get_parameter(request.POST.get('expert_id'), para_intro='专家ID'
                                  , allow_null=True, default='')
        page = get_parameter(request.POST.get('page'), para_intro='分页：查询第几页'
                             , valid_check=INTEGER_POSITIVE)
        rows = get_parameter(request.POST.get('rows'), para_intro='分页：每页记录数'
                             , valid_check=INTEGER_IN_RANGE, min=1, max=50)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    # 置顶的最前显示，其次按发布时间先后显示
    article_qs = SiteArticle.objects.filter(is_delete=False).order_by('-is_top', '-publish_time', '-create_time')
    if expert_id:
        article_qs = article_qs.filter(expert_id=expert_id)

    if title_key != '':
        article_qs = article_qs.filter(title__icontains=title_key)

    # 依照'是否被推送'进行过滤
    article_list = list()

    for each_article in article_qs:

        # 处理一些可能为空的属性
        publish_time = each_article.publish_time or each_article.create_time
        if each_article.admit_user:
            admit_user_id = str(each_article.admit_user.id)
            admit_user_name = each_article.admit_user.name
        else:
            admit_user_id = ''
            admit_user_name = ''
        if each_article.admit_time:
            admit_time = utils_common.datetime2str(each_article.admit_time)
        else:
            admit_time = ''

        article_list.append({
            'id': str(each_article.id),
            'title': each_article.title,
            'publish_user_id': str(each_article.publish_user.id),
            'publish_user_name': each_article.publish_user.name,
            'publish_time': utils_common.datetime2str(publish_time),
            'click': str(each_article.click),
            'admit_state': str(each_article.admit_status),
            'admit_user_id': admit_user_id,
            'admit_user_name': admit_user_name,
            'admit_time': admit_time,
            'is_top': utils_common.bool2str(each_article.is_top),
            'author': each_article.author,
            'image': services.get_article_cover(each_article),
            'expert_name': each_article.expert.expert_name if each_article.expert else '',
        })

    pager = Paginator(article_list, int(rows))
    if int(page) > int(pager.num_pages):
        return utils_common.response(get_msg(ARTICLE_PAGER_OUT_OF_INDEX))
    result = {
        'page': page,
        'total': pager.num_pages,
        'records': pager.count,
        'rows': [each for each in pager.page(page)]
    }
    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": result}
    return utils_common.response(dict_resp)


@require_POST
def manage_expert_list(request):
    """
        查询专家列表
    """
    try:
        key = get_parameter(request.POST.get('key'), para_intro='搜索关键字', allow_null=True, default='')
        page = get_parameter(request.POST.get('page'), para_intro='分页：查询第几页', allow_null=True, default='')
        rows = get_parameter(request.POST.get('rows'), para_intro='分页：每页记录数', allow_null=True, default='')
        # rows = get_parameter(request.POST.get('rows'), para_intro='分页：每页记录数', valid_check=INTEGER_IN_RANGE, min=1, max=100)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    try:
        data = services.manage_expert_list(key, page, rows)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)

    return utils_common.response({'c': REQUEST_SUCCESS[0], 'm': REQUEST_SUCCESS[1], 'd': data})


@require_POST
def manage_expert_get(request):
    """
        查询单个专家
    """
    try:
        expert_id = get_parameter(request.POST.get('expert_id'), para_intro='专家ID', allow_null=False)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    try:
        data = services.manage_expert_get(expert_id)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)

    return utils_common.response({'c': REQUEST_SUCCESS[0], 'm': REQUEST_SUCCESS[1], 'd': data})


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_expert_add(request):
    """
        添加专家
    """
    try:
        expert_name = get_parameter(request.POST.get('expert_name'), para_intro='专家姓名', allow_null=False)
        expert_sortorder = get_parameter(request.POST.get('expert_sortorder'), para_intro='专家排序', allow_null=True, default='100')
        expert_image = request.FILES.get('expert_image')
        expert_intro = get_parameter(request.POST.get('expert_intro'), para_intro='专家介绍', allow_null=True)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    try:
        data = services.manage_expert_add(expert_name, expert_sortorder, expert_image, expert_intro)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)

    return utils_common.response({'c': REQUEST_SUCCESS[0], 'm': REQUEST_SUCCESS[1], 'd': data})


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_expert_edit(request):
    """
        修改专家资料
    """
    try:
        expert_id = get_parameter(request.POST.get('expert_id'), para_intro='专家ID', allow_null=False)
        expert_name = get_parameter(request.POST.get('expert_name'), para_intro='专家姓名', allow_null=False)
        expert_sortorder = get_parameter(request.POST.get('expert_sortorder'), para_intro='专家排序', allow_null=True, default='100')
        expert_image = request.FILES.get('expert_image')
        expert_intro = get_parameter(request.POST.get('expert_intro'), para_intro='专家介绍', allow_null=True)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    try:
        data = services.manage_expert_edit(expert_id, expert_name, expert_sortorder, expert_image, expert_intro)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)

    return utils_common.response({'c': REQUEST_SUCCESS[0], 'm': REQUEST_SUCCESS[1], 'd': data})


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_expert_delete(request):
    """
        批量删除专家
    """
    try:
        id_list = get_parameter(request.POST.get('id_list'), para_intro='专家的ID号列表', allow_null=False)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    try:
        data = services.manage_expert_delete(id_list)
    except Exception as e:
        logger.exception(e)
        return response_exception(e)

    return utils_common.response({'c': REQUEST_SUCCESS[0], 'm': REQUEST_SUCCESS[1], 'd': data})


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_article_pend_list(request):
    try:
        title_key = get_parameter(request.POST.get('title_key'), para_intro='标题关键字'
                                  , allow_null=True, default='')
        page = get_parameter(request.POST.get('page'), para_intro='页码'
                             , valid_check=INTEGER_POSITIVE)
        rows = get_parameter(request.POST.get('rows'), para_intro='每页记录数'
                             , valid_check=INTEGER_IN_RANGE, min=1, max=50)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    articles = SiteArticle.objects.filter(is_delete=False, admit_status=int(DB_ARTICLE_ADMIT_STATE_PEND)) \
        .order_by('-publish_time')

    # 按照关键字过滤
    if title_key != '':
        articles = articles.filter(title__icontains=title_key)

    pager = Paginator(articles, int(rows))

    if int(page) > int(pager.num_pages):
        return utils_common.response(get_msg(ARTICLE_PAGER_OUT_OF_INDEX))

    range_records = pager.page(page)
    rows = list()
    for each_record in range_records:
        rows.append({
            'id': str(each_record.id),
            'title': each_record.title,
            'publish_user_id': str(each_record.publish_user.id),
            'publish_user_name': each_record.publish_user.name,
            'publish_time': utils_common.datetime2str(each_record.publish_time),
        })

    result = {
        'page': page,
        'total': pager.num_pages,
        'records': pager.count,
        'rows': rows
    }

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": result}
    return utils_common.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_article_push_list(request):
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='推送栏目的ID编号')
#         admit_state = get_parameter(
#                     request.POST.get('admit_state'), para_intro='审核状态', allow_null=True, default='', valid_check=CHOICES
#                     , choices=(str(DB_ARTICLE_ADMIT_STATE_PEND), str(DB_ARTICLE_ADMIT_STATE_PASS), str(DB_ARTICLE_ADMIT_STATE_FAIL)))
#         title_key = get_parameter(request.POST.get('title_key'), para_intro='标题关键字', allow_null=True, default='')
#         page = get_parameter(request.POST.get('page'), para_intro='页码', valid_check=INTEGER_POSITIVE)
#         rows = get_parameter(request.POST.get('rows'), para_intro='每页记录数', valid_check=INTEGER_IN_RANGE, min=1, max=50)
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     push_articles = SitePushArticle.objects.filter(push_channel__id=id).order_by(
#                                                                                  '-push_article__publish_time',
#                                                                                  '-push_article__create_time',
#                                                                                  '-create_time')
#
#     # 按照审核状态过滤
#     if admit_state != '':
#         push_articles = push_articles.filter(push_article__admit_status=int(admit_state))
#     # 按照关键字过滤
#     if title_key != '':
#         push_articles = push_articles.filter(push_article__title__icontains=title_key)
#
#     pager = Paginator(push_articles, int(rows))
#
#     if int(page) > int(pager.num_pages):
#         return utils.response(get_msg(ARTICLE_PAGER_OUT_OF_INDEX))
#
#     range_records = pager.page(page)
#     rows = list()
#     for each_record in range_records:
#         if each_record.push_article.admit_user:
#             admit_user_id = str(each_record.push_article.admit_user.id)
#             admit_user_name = each_record.push_article.admit_user.name
#             admit_time = utils.datetime2str(each_record.push_article.admit_time)
#         else:
#             admit_user_id = ''
#             admit_user_name = ''
#             admit_time = ''
#         rows.append({
#             'id': str(each_record.id),
#             'title': each_record.push_article.title,
#             'publish_user_id': str(each_record.push_article.publish_user.id),
#             'publish_user_name': each_record.push_article.publish_user.name,
#             'publish_time': utils.datetime2str(each_record.push_article.publish_time),
#             'click': str(each_record.push_article.click),
#             'admit_state': str(each_record.push_article.admit_status),
#             'admit_user_id': admit_user_id,
#             'admit_user_name': admit_user_name,
#             'admit_time' : admit_time,
#             'is_top': utils.bool2str(each_record.push_article.is_top),
#             'category_id': str(each_record.push_article.category.id),
#             'category_name': each_record.push_article.category.name,
#             'channel_id': str(each_record.push_article.category.channel.id),
#             'channel_name': each_record.push_article.category.channel.name,
#             'push_time': utils.datetime2str(each_record.create_time)
#         })
#
#     result = {
#         'page': page,
#         'total': pager.num_pages,
#         'records': pager.count,
#         'rows': rows
#     }
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": result}
#     return utils.response(dict_resp)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_component_list(request):
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.load_components()}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_component_add(request):
#     try:
#         key = get_parameter(request.POST.get('key'), para_intro='组件关键字')
#         name = get_parameter(request.POST.get('name'), allow_null=True, default='', para_intro='组件名称')
#         intro = get_parameter(request.POST.get('intro'), para_intro='描述', allow_null=True, default='')
#         image_file = request.FILES.get('image')
#         link = get_parameter(request.POST.get('link'), para_intro='链接', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接' \
#                                          , allow_null=True, default=FALSE, valid_check=CHOICES, choices=(TRUE, FALSE))
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 组件关键字不能重复
#     occupied_key_list = services.load_occupied_component_key()
#     if key in occupied_key_list:
#         return utils.response(
#             {'c': COMPONENT_OCCUPIED_KEY[0], 'm': COMPONENT_OCCUPIED_KEY[1] % ' | '.join(occupied_key_list)})
#
#     new_component = SiteComponent()
#     new_component.key = key
#     new_component.name = name
#     new_component.intro = intro
#     new_component.image = image_file
#     new_component.link = link
#     new_component.is_link_out_open = utils.str2bool(is_link_out_open)
#     new_component.is_delete = False
#     new_component.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)
#
#
# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_component_delete(request):
#     try:
#         id_list = get_parameter(request.POST.get('id_list'), para_intro='组件ID编号列表')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     components_del=list()
#     for eachid in id_list.split(','):
#         # 检查该组件是否存在
#         components_qs = SiteComponent.objects.filter(is_delete=False, id=eachid)
#         if not components_qs.exists():
#             return utils.response(get_msg(COMPONENT_NOT_FOUND))
#         this_component = components_qs.first()
#
#         # 检查该组件是否被门户首页引用
#         if services.is_cpnt_key_ref(this_component.key):
#             return utils.response(get_msg(COMPONENT_REF_BY_HOMEPAGE))
#         components_del.append(this_component)
#
#     for eachcomponent in components_del:
#         eachcomponent.is_delete = True
#         eachcomponent.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)
#
#
# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_component_edit(request):
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='组件ID编号', valid_check=INTEGER_NONNEGATIVE)
#         key = get_parameter(request.POST.get('key'), para_intro='组件关键字')
#         name = get_parameter(request.POST.get('name'), allow_null=True, default='', para_intro='组件名称')
#         intro = get_parameter(request.POST.get('intro'), para_intro='描述', allow_null=True, default='')
#         image_file = request.FILES.get('image')
#         link = get_parameter(request.POST.get('link'), para_intro='链接', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接' \
#                                          , allow_null=True, default=FALSE, valid_check=CHOICES, choices=(TRUE, FALSE))
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查该组件是否存在
#     components_qs = SiteComponent.objects.filter(is_delete=False, id=id)
#     if not components_qs.exists():
#         return utils.response(get_msg(COMPONENT_NOT_FOUND))
#     this_component = components_qs.first()
#
#     # 组件关键字不能重复
#     if key != this_component.key:
#         occupied_key_list = services.load_occupied_component_key()
#         if key in occupied_key_list:
#             return utils.response(
#                 {'c': COMPONENT_OCCUPIED_KEY[0], 'm': COMPONENT_OCCUPIED_KEY[1] % ' | '.join(occupied_key_list)})
#
#     this_component.key = key
#     this_component.name = name
#     this_component.intro = intro
#     if image_file:
#         this_component.image = image_file
#     this_component.link = link
#     this_component.is_link_out_open = utils.str2bool(is_link_out_open)
#     this_component.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_article_get(request):
    """
        获取某一文章正文
        api/manage/article/get
    """
    try:
        id = get_parameter(request.POST.get('id'), para_intro='文章ID', valid_check=INTEGER_NONNEGATIVE)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.get_article_by_pk(id)}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_article_preview(request):
    """
        获取某一文章预览
        api/manage/article/preview
    """
    try:
        is_preview = get_parameter(request.POST.get('is_preview'), para_intro='是否预览', allow_null=True, default=FALSE,
                                   valid_check=CHOICES, choices=(TRUE, FALSE))
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1],
                 "d": services.get_article_preview_by_user(request.user)}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_article_add(request):
    """
        发文
        api/manage/article/add
    """
    # 检查参数
    try:
        title = get_parameter(request.POST.get('title'), para_intro='文章标题')
        subtitle = get_parameter(request.POST.get('subtitle'), para_intro='文章子标题', allow_null=True, default='')
        intro = get_parameter(request.POST.get('intro'), para_intro='摘要', allow_null=True, default='')
        image_file = request.FILES.get('image')
        image_url = get_parameter(request.POST.get('image_url'), para_intro='图片路径', allow_null=True, default='')
        video_upload_id = get_parameter(request.POST.get('video_upload_id'), para_intro='上传的视频ID', allow_null=True, default='')
        expert_id = get_parameter(request.POST.get('expert_id'), para_intro='专家ID', allow_null=True, default='')
        pdf_upload_id = request.POST.get('pdf_upload_id')
        content = get_parameter(request.POST.get('content'), para_intro='正文', allow_null=True, default='')
        publish_time = get_parameter(request.POST.get('publish_time'), para_intro='发布时间', allow_null=True, default=None)
        author = get_parameter(request.POST.get('author'), para_intro='作者', allow_null=True, default='')
        is_preview = get_parameter(request.POST.get('is_preview'), para_intro='是否预览', allow_null=True, default=FALSE,
                                   valid_check=CHOICES, choices=(TRUE, FALSE))

    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    # 处理正文中的图片
    if is_preview == FALSE:
        # 临时图片和附件转正式图片和附件
        re_search_result = re.findall(r'(href|src)=\"(/media/temp/20[0-9]{4}/(image|file|video)/.*?)\"', content)
        if re_search_result:
            for each_find in re_search_result:

                each_temp = each_find[1]
                original_path = settings.BASE_DIR + each_temp
                converted_path = settings.BASE_DIR + (each_temp.replace('temp', 'article'))
                if not os.path.exists(os.path.dirname(converted_path)):
                    os.makedirs(os.path.dirname(converted_path))

                # 将临时文件从临时区域移动到正式存储区域
                if os.path.exists(original_path):
                    shutil.move(original_path, converted_path)

            # 替换原content中temp的部分
            content = re.compile(r'(/media/)(temp)(/20[0-9]{4}/(image|file|video)/)').sub(r'\1article\3', content)

    # 普通文章发文要特殊处理封面image
    if is_preview == FALSE and image_url:
        # 从本地新增一张图片
        if TEMP_IMAGE in image_url:
            image_url = unquote(str(image_url)).decode('utf8')
            ABS_BASE_DIR = os.path.abspath(BASE_DIR)
            permanent_cover_path = ARTICLE_COVER % (datetime.now().strftime('%Y%m'), image_url.split('/')[-1])
            if not os.path.exists(os.path.dirname(ABS_BASE_DIR + '/media/' + permanent_cover_path)):
                os.makedirs(os.path.dirname(ABS_BASE_DIR + '/media/' + permanent_cover_path))
            shutil.move(ABS_BASE_DIR+image_url, ABS_BASE_DIR + '/media/' + permanent_cover_path)
            image_file = permanent_cover_path
        # 从content中选择一张图片
        else:
            image_url = unquote(str(image_url)).decode('utf8')
            image_file = image_url.replace('/media/temp/', '/media/article/')

    # # 检查发的各个栏目的类型需要统一
    # cate_list = list()
    # cate_type_list = list()
    # for each_category in category_list.rstrip(',').split(','):
    #     cate = SiteCategory.objects.filter(is_delete=False, id=int(each_category)).first()
    #     if not cate:
    #         continue
    #     cate_type_list.append(cate.type.id)
    #     cate_list.append(cate)
    # if len(set(cate_type_list)) != 1:
    #     return utils.response(get_msg(ARTICLE_DIFFERENT_CATE_TYPE))

    # 保存新文章
    new_article = SiteArticle()
    new_article.title = title
    new_article.subtitle = subtitle
    new_article.intro = intro
    new_article.image = image_file
    new_article.video_id = video_upload_id if video_upload_id else ''
    new_article.expert_id = expert_id if expert_id else ''
    new_article.content = content
    new_article.publish_user = request.user
    new_article.author = author

    # 如果用户不显式的指定发布时间，则取当前服务器时间作为发布时间
    if publish_time == '':
        new_article.publish_time = datetime.now()
    else:
        new_article.publish_time = utils_common.str2datetime(publish_time)

    # 如果是管理员则自动审核通过
    if request.user.role == DB_USER_ROLE_ADMIN:
        new_article.admit_status = DB_ARTICLE_ADMIT_STATE_PASS
        new_article.admit_time = datetime.now()
        new_article.admit_user = request.user
    else:
        new_article.admit_status = DB_ARTICLE_ADMIT_STATE_PEND

    # 如果是预览，则先删除原来的预览文章
    if is_preview == TRUE:
        old_pre_article = SiteArticle.objects.filter(is_delete=True, author__startswith='preview_' + str(request.user.id) + '_').first()
        if old_pre_article:
            new_article.id = old_pre_article.id
            old_pre_article.delete()
        new_article.is_delete = True
        new_article.author = 'preview_' + str(request.user.id) + '_' + author

    new_article.save()
    # 重新计算专家文章数量
    services.expert_articlenum_update(new_article.expert_id)

    # 将PDF文件改名为ID.pdf的格式，同时生成swf文件
    if pdf_upload_id:
        pdf_chunked_upload_temp_path = os.path.join(CHUNKED_UPLOAD_PATH, pdf_upload_id+'.part')

        pdf_permament_folder = utils_common.safe_folder(BASE_DIR + '/media/journal/pdf/')
        pdf_permament_path = pdf_permament_folder + str(new_article.id) + '.pdf'

        swf_permament_home_folder = utils_common.safe_folder(BASE_DIR + '/media/journal/swf/')
        swf_permament_folder = utils_common.safe_folder(swf_permament_home_folder + str(new_article.id))

        # 如果临时刊物文件不存在，则抛出异常
        if not os.path.exists(pdf_chunked_upload_temp_path):
            return utils_common.response(get_msg(ARTICLE_JOURNAL_UPLOAD_FAIL))

        # part文件改名pdf
        shutil.move(pdf_chunked_upload_temp_path, pdf_permament_path)

        if os.name == 'nt':
            os.popen(BASE_DIR + '/utils/3party/pdf2swf.exe ' + pdf_permament_path + ' ' + swf_permament_folder
                                + '/%.swf -f -T 9')
        else:
            os.popen('nohup /usr/swftools/bin/pdf2swf ' + pdf_permament_path + ' ' + swf_permament_folder
                                + '/%.swf -f -T 9 -s languagedir=/usr/local/xpdf-chinese-simplified/ &')
    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_article_edit(request):
    """
        修改文章
        api/manage/article/edit
    """
    # 检查参数
    try:
        id = get_parameter(request.POST.get('id'), para_intro='文章ID编号', valid_check=INTEGER_NONNEGATIVE)
        title = get_parameter(request.POST.get('title'), para_intro='文章标题')
        subtitle = get_parameter(request.POST.get('subtitle'), para_intro='文章子标题', allow_null=True, default='')
        intro = get_parameter(request.POST.get('intro'), para_intro='摘要', allow_null=True, default='')
        image_file = request.FILES.get('image')
        image_url = get_parameter(request.POST.get('image_url'), para_intro='图片路径', allow_null=True, default='')
        pdf_upload_id = request.POST.get('pdf_upload_id')
        video_upload_id = get_parameter(request.POST.get('video_upload_id'), para_intro='上传的视频ID', allow_null=True, default='')
        expert_id = get_parameter(request.POST.get('expert_id'), para_intro='专家ID', allow_null=True, default='')
        content = get_parameter(request.POST.get('content'), para_intro='正文', allow_null=True, default='')
        publish_time = get_parameter(request.POST.get('publish_time'), para_intro='发布时间', allow_null=True, default=None)
        is_delete_image = get_parameter(request.POST.get('is_delete_image'), para_intro='是否清除文章封面' \
                                     , allow_null=True, default=FALSE, valid_check=CHOICES, choices=(TRUE, FALSE))
        author = get_parameter(request.POST.get('author'), para_intro='作者', allow_null=True, default='')
        is_preview = get_parameter(request.POST.get('is_preview'), para_intro='是否预览', allow_null=True, default=FALSE,
                                   valid_check=CHOICES, choices=(TRUE, FALSE))
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    article = SiteArticle.objects.filter(is_delete=False, id=id).first()
    if not article:
        return utils_common.response(get_msg(ARTICLE_ID_INVALID))
    old_article_expert_id = article.expert_id

    # 检查审核状态，非管理员不允许修改已经审核通过的文章。
    if (article.admit_status == DB_ARTICLE_ADMIT_STATE_PASS) and (request.user.role != DB_USER_ROLE_ADMIN):
        return utils_common.response(get_msg(ARTICLE_PASS_CANNOT_MODI))

    # 临时图片和附件转正式图片和附件
    if is_preview == FALSE:
        re_search_result = re.findall(r'(href|src)=\"(/media/temp/20[0-9]{4}/(image|file|video)/.*?)\"', content)
        if re_search_result:
            for each_find in re_search_result:
                each_temp = each_find[1]
                original_path = settings.BASE_DIR + each_temp
                converted_path = settings.BASE_DIR + (each_temp.replace('temp', 'article'))
                if not os.path.exists(os.path.dirname(converted_path)):
                    os.makedirs(os.path.dirname(converted_path))

                # 将临时文件从临时区域移动到正式存储区域
                if os.path.exists(original_path):
                    shutil.move(original_path, converted_path)

            # 替换原content中temp的部分
            content = re.compile(r'(/media/)(temp)(/20[0-9]{4}/(image|file|video)/)').sub(r'\1article\3', content)

    article.title = title
    article.subtitle = subtitle
    article.intro = intro
    article.content = content
    article.author = author
    article.video_id = video_upload_id
    article.expert_id = expert_id

    if is_preview == FALSE:
        if is_delete_image == '1':
            article.image = None
        else:
            if image_url:
                # 普通文章修改要特殊处理封面image
                # 从本地新增一张图片
                if TEMP_IMAGE in image_url:
                    image_url = unquote(str(image_url)).decode('utf8')
                    # image_url = unquote(image_url.encode('utf8'))
                    ABS_BASE_DIR = os.path.abspath(BASE_DIR)
                    permanent_cover_path = ARTICLE_COVER % (datetime.now().strftime('%Y%m'), image_url.split('/')[-1])
                    if not os.path.exists(os.path.dirname(ABS_BASE_DIR + '/media/' + permanent_cover_path)):
                        os.makedirs(os.path.dirname(ABS_BASE_DIR + '/media/' + permanent_cover_path))
                    shutil.move(ABS_BASE_DIR + image_url, ABS_BASE_DIR + '/media/' + permanent_cover_path)
                    image_file = permanent_cover_path
                # 从content中选择一张图片
                else:
                    image_url = unquote(str(image_url)).decode('utf8')
                    image_file = image_url.replace('/media/temp/', '/media/article/')
            else:
                pass
            if image_file:
                article.image = image_file.encode('utf8')

    # 当用户为老师，且文章为未通过状态时，修改后将状态改为待审核
    if (article.admit_status == DB_ARTICLE_ADMIT_STATE_FAIL) and (request.user.role != DB_USER_ROLE_ADMIN):
        article.admit_status = DB_ARTICLE_ADMIT_STATE_PEND

    # 如果用户不显式的指定发布时间，则取当前服务器时间作为发布时间
    if publish_time != '':
        article.publish_time = utils_common.str2datetime(publish_time)

    if is_preview == TRUE:
        old_pre_article = SiteArticle.objects.filter(is_delete=True,
                                                     author__startswith='preview_' + str(request.user.id) + '_').first()
        if old_pre_article:
            article.id = old_pre_article.id
            old_pre_article.delete()
        else:
            article.id = None
        article.is_delete = True
        article.author = 'preview_' + str(request.user.id) + '_' + author

    article.save()

    # 重新计算原文章专家及新文章专家数量
    services.expert_articlenum_update(old_article_expert_id)
    services.expert_articlenum_update(article.expert_id)

    # 将PDF文件改名为ID.pdf的格式，同时生成swf文件
    if pdf_upload_id:
        pdf_chunked_upload_temp_path = os.path.join(CHUNKED_UPLOAD_PATH, pdf_upload_id+'.part')

        pdf_permament_folder = utils_common.safe_folder(BASE_DIR + '/media/journal/pdf/')
        pdf_permament_path = pdf_permament_folder + id + '.pdf'

        swf_permament_home_folder = utils_common.safe_folder(BASE_DIR + '/media/journal/swf/')
        swf_permament_folder = utils_common.safe_folder(swf_permament_home_folder + id)

        # 备份原pdf文件，清空原来转换后的swf
        if os.path.exists(pdf_permament_path):
            shutil.move(pdf_permament_path, pdf_permament_path + '.' + datetime.now().strftime("%Y%m%d%H%M%S"))
        shutil.rmtree(swf_permament_folder)
        os.makedirs(swf_permament_folder)

        # 如果临时刊物文件不存在，则抛出异常
        if not os.path.exists(pdf_chunked_upload_temp_path):
            return utils_common.response(get_msg(ARTICLE_JOURNAL_UPLOAD_FAIL))

        # part文件改名pdf
        shutil.move(pdf_chunked_upload_temp_path, pdf_permament_path)

        if os.name == 'nt':
            os.popen(BASE_DIR + '/utils/3party/pdf2swf.exe ' + pdf_permament_path + ' ' + swf_permament_folder
                                + '/%.swf -f -T 9')
        else:
            os.popen('nohup /usr/swftools/bin/pdf2swf ' + pdf_permament_path + ' ' + swf_permament_folder
                                + '/%.swf -f -T 9 -s languagedir=/usr/local/xpdf-chinese-simplified/ &')

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_article_push(request):
#     try:
#         article_id_list = get_parameter(request.POST.get('article_id_list'), para_intro='文章ID编号列表')
#         push_channel_id = get_parameter(request.POST.get('push_channel_id'), para_intro='推送到的栏目ID' \
#                                     , valid_check=INTEGER_NONNEGATIVE)
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     push_channel = SitePushChannel.objects.filter(is_delete=False, id=push_channel_id).first()
#     if not push_channel:
#         return utils.response(get_msg(CHANNEL_PUSH_INVALID))
#
#     for each_article_id in article_id_list.split(','):
#         article = SiteArticle.objects.filter(is_delete=False, id=each_article_id).first()
#         if not article:
#             continue
#         if not article.category.type.is_allow_push:
#             logger.warn(u'文章"%s"所在栏目不支持推送' % article.title)
#             continue
#         if SitePushArticle.objects.filter(push_article=article, push_channel=push_channel).exists():
#             logger.warn(u'文章"%s"之前已经被推送到了栏目"%s"，不可重复推送' % (article.title, push_channel.name))
#             continue
#
#         push_article = SitePushArticle()
#         push_article.push_article = article
#         push_article.push_channel = push_channel
#         push_article.push_user = request.user
#         push_article.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_article_cancelpush(request):
#     try:
#         push_article_id_list = get_parameter(request.POST.get('push_article_id_list'), para_intro='推送文章ID编号列表')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     for each_push_article_id in push_article_id_list.split(','):
#         push_article = SitePushArticle.objects.filter(id=each_push_article_id).first()
#         if not push_article:
#             continue
#         push_article.delete()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_article_delete(request):
    try:
        id_list = get_parameter(request.POST.get('id_list'), para_intro='要删除的文章ID编号列表')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    article_list = list()
    for each_id in id_list.split(','):
        article = SiteArticle.objects.filter(is_delete=False, id=int(each_id)).first()
        if article:
            if request.user.role == DB_USER_ROLE_TEACHER:
                # 老师只能删除自己的文章
                if article.publish_user != request.user:
                    return utils_common.response(get_msg(ARTICLE_TEACHER_ONLY_CAN_DELETE_SELF))
                # 老师只能删除待审核和未审核的文章
                if article.admit_status == DB_ARTICLE_ADMIT_STATE_PASS:
                    return utils_common.response(get_msg(ARTICLE_PASS_CANNOT_DELETE))
            article_list.append(article)
    for each_article in article_list:
        each_article.is_delete = True
        each_article.save()
        # 重新计算专家文章数量
        services.expert_articlenum_update(each_article.expert_id)

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_article_top(request):
    try:
        id_list = get_parameter(request.POST.get('id_list'), para_intro='要置顶的文章ID编号列表')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    article_list = list()
    for each_id in id_list.split(','):
        article = SiteArticle.objects.filter(is_delete=False, id=int(each_id)).first()
        if article:
            if article.is_top:
                continue
            article_list.append(article)
    for each_article in article_list:
        each_article.is_top=True
        each_article.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_article_untop(request):
    try:
        id_list = get_parameter(request.POST.get('id_list'), para_intro='要取消置顶的文章ID编号列表')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    article_list = list()
    for each_id in id_list.split(','):
        article = SiteArticle.objects.filter(is_delete=False, id=int(each_id)).first()
        if article:
            if not article.is_top:
                continue
            article_list.append(article)
    for each_article in article_list:
        each_article.is_top=False
        each_article.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_article_pass(request):
    try:
        id_list = get_parameter(request.POST.get('id_list'), para_intro='要审核的文章ID编号列表')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    article_list = list()
    for each_id in id_list.split(','):
        article = SiteArticle.objects.filter(is_delete=False, id=int(each_id)).first()
        if article:
            if article.admit_status == DB_ARTICLE_ADMIT_STATE_PASS:
                continue
            article_list.append(article)
    for each_article in article_list:
        each_article.admit_status = DB_ARTICLE_ADMIT_STATE_PASS
        each_article.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_article_failpass(request):
    try:
        id_list = get_parameter(request.POST.get('id_list'), para_intro='要设置不通过的文章ID编号列表')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    article_list = list()
    for each_id in id_list.split(','):
        article = SiteArticle.objects.filter(is_delete=False, id=int(each_id)).first()
        if article:
            if article.admit_status == DB_ARTICLE_ADMIT_STATE_FAIL:
                continue
            article_list.append(article)
    for each_article in article_list:
        each_article.admit_status = DB_ARTICLE_ADMIT_STATE_FAIL
        each_article.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_quickfunc_list(request):
#     """
#         获取所有的快速功能链接
#         api/manage/quickfunc/list
#     """
#     quicks_all = services.load_quickfunc(only_show_active=False)
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": quicks_all}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_quickfunc_add(request):
#     """
#         新增一个快速功能链接
#         api/manage/quickfunc/add
#     """
#     try:
#         name = get_parameter(request.POST.get('name'), allow_null=True, default='', para_intro='快速功能链接名称')
#         intro = get_parameter(request.POST.get('intro'), para_intro='描述', allow_null=True, default='')
#         image_file = request.FILES.get('image')
#         sort = get_parameter(request.POST.get('sort'), para_intro='排序' \
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default=CHANNEL_SORT_DEFAULT)
#         is_active = get_parameter(request.POST.get('is_active'), para_intro='是否有效'
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#         link = get_parameter(request.POST.get('link'), para_intro='链接', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接' \
#                                          , allow_null=True, default=FALSE, valid_check=CHOICES, choices=(TRUE, FALSE))
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     new_quick = SiteQuickFunc()
#     new_quick.is_delete = False
#     new_quick.name = name
#     new_quick.intro = intro
#     new_quick.image = image_file
#     new_quick.sort = int(sort)
#     new_quick.is_active = utils.str2bool(is_active)
#     new_quick.link = link
#     new_quick.is_link_out_open = utils.str2bool(is_link_out_open)
#     new_quick.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_quickfunc_edit(request):
#     """
#         修改一个快速功能链接
#         api/manage/quickfunc/edit
#     """
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='快速功能链接ID编号', valid_check=INTEGER_NONNEGATIVE)
#         name = get_parameter(request.POST.get('name'), allow_null=True, default='', para_intro='快速功能链接名称')
#         intro = get_parameter(request.POST.get('intro'), para_intro='描述', allow_null=True, default='')
#         image_file = request.FILES.get('image')
#         sort = get_parameter(request.POST.get('sort'), para_intro='排序' \
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default=CHANNEL_SORT_DEFAULT)
#         is_active = get_parameter(request.POST.get('is_active'), para_intro='是否有效'
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default='1')
#         link = get_parameter(request.POST.get('link'), para_intro='链接', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接' \
#                                          , allow_null=True, default=FALSE, valid_check=CHOICES, choices=(TRUE, FALSE))
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查该ID是否存在
#     quick = SiteQuickFunc.objects.filter(is_delete=False, pk=id).first()
#     if not quick:
#         return utils.response(get_msg(QUICKFUNC_ID_INVALID))
#
#     quick.name = name
#     quick.intro = intro
#     if image_file:
#         quick.image = image_file
#     quick.sort = int(sort)
#     quick.is_active = utils.str2bool(is_active)
#     quick.link = link
#     quick.is_link_out_open = utils.str2bool(is_link_out_open)
#     quick.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_quickfunc_delete(request):
#     """
#         删除一个快速功能链接
#         api/manage/quickfunc/delete
#     """
#     try:
#         id_list = get_parameter(request.POST.get('id_list'), para_intro='快速功能链接ID编号列表')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     quickfunclist = list()
#     for eachid in id_list.split(','):
#         # 检查该ID是否存在
#         quick = SiteQuickFunc.objects.filter(is_delete=False, pk=eachid).first()
#         if not quick:
#             return utils.response(get_msg(QUICKFUNC_ID_INVALID))
#         quickfunclist.append(quick)
#
#     for eachquick in quickfunclist:
#         eachquick.is_delete = True
#         eachquick.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_picture_add(request):
#     """
#         新增一个轮播图
#         api/manage/picture/add
#     """
#     try:
#         title = get_parameter(request.POST.get('title'), allow_null=True, default='', para_intro='轮播图标题')
#         intro = get_parameter(request.POST.get('intro'), para_intro='描述', allow_null=True, default='')
#         image_file = request.FILES.get('image')
#         sort = get_parameter(request.POST.get('sort'), para_intro='排序' \
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default=CHANNEL_SORT_DEFAULT)
#         link = get_parameter(request.POST.get('link'), para_intro='链接', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接' \
#                                          , allow_null=True, default=FALSE, valid_check=CHOICES, choices=('0', '1'))
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     if not image_file:
#         return utils.response(get_msg(PICTURE_NOPIC))
#
#     new_pic = SitePicture()
#     new_pic.is_delete = False
#     new_pic.title = title
#     new_pic.intro = intro
#     new_pic.image = image_file
#     new_pic.sort = int(sort)
#     new_pic.link = link
#     new_pic.is_link_out_open = utils.str2bool(is_link_out_open)
#     new_pic.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_picture_edit(request):
#     """
#         新增一个轮播图
#         api/manage/picture/edit
#     """
#     try:
#         id = get_parameter(request.POST.get('id'), para_intro='轮播图ID编号', valid_check=INTEGER_NONNEGATIVE)
#         title = get_parameter(request.POST.get('title'), allow_null=True, default='', para_intro='轮播图标题')
#         intro = get_parameter(request.POST.get('intro'), para_intro='描述', allow_null=True, default='')
#         image_file = request.FILES.get('image')
#         sort = get_parameter(request.POST.get('sort'), para_intro='排序' \
#                                   , valid_check=INTEGER_NONNEGATIVE, allow_null=True, default=CHANNEL_SORT_DEFAULT)
#         link = get_parameter(request.POST.get('link'), para_intro='链接', allow_null=True, default='')
#         is_link_out_open = get_parameter(request.POST.get('is_link_out_open'), para_intro='是否在新窗口打开链接' \
#                                          , allow_null=True, default=FALSE, valid_check=CHOICES, choices=(TRUE, FALSE))
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     # 检查该ID是否存在
#     pic = SitePicture.objects.filter(is_delete=False, pk=id).first()
#     if not pic:
#         return utils.response(get_msg(PICTURE_ID_INVALID))
#
#     pic.title = title
#     pic.intro = intro
#     if image_file:
#         pic.image = image_file
#     pic.sort = int(sort)
#     pic.link = link
#     pic.is_link_out_open = utils.str2bool(is_link_out_open)
#     try:
#         pic.save()
#     except:
#         return utils.response(get_msg(PICTURE_SAVE_FAIL))
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


# @require_POST
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_picture_delete(request):
#     """
#         删除一个轮播图
#         api/manage/picture/delete
#     """
#     try:
#         id_list = get_parameter(request.POST.get('id_list'), para_intro='轮播图ID编号列表')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     picturelist = list()
#     for eachid in id_list.split(','):
#         # 检查该ID是否存在
#         picture = SitePicture.objects.filter(is_delete=False, pk=eachid).first()
#         if not picture:
#             return utils.response(get_msg(PICTURE_ID_INVALID))
#         picturelist.append(picture)
#
#     for eachpicture in picturelist:
#         eachpicture.is_delete = True
#         eachpicture.save()
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
#     return utils.response(dict_resp)


if __name__ == '__main__':
    pass