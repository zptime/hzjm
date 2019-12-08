# -*- coding: utf-8 -*-

import logging

from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_GET

import services
from app_common.models import CommonParameter
from app_site.models import *
from utils.err_code import *
from utils.para_check import *
from utils import utils_common
from utils.utils_common import respformat

logger = logging.getLogger(__name__)

#
# @require_POST
# def portal_component_get(request):
#     """
#         获取一个基础组件
#     """
#     try:
#         component_key = get_parameter(request.POST.get('key'), para_intro='组件关键字')
#     except InvalidParaException as ipe:
#         return utils.response(respformat(ipe.message))
#
#     component = services.get_component_by_key(component_key)
#     if not component:
#         return utils.response(get_msg(COMPONENT_NOT_FOUND))
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": component}
#     return utils.response(dict_resp)


# @require_GET
# def portal_picture_list(request):
#     """
#         获取所有的轮播图
#     """
#     pictures_all = services.load_all_picture()
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": pictures_all}
#     return utils.response(dict_resp)


# @require_GET
# def portal_quickfunc_list(request):
#     """
#         获取所有的快速功能链接
#     """
#     quicks_all = services.load_quickfunc()
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": quicks_all}
#     return utils.response(dict_resp)


@require_POST
def portal_article_get(request):
    """
        获取某一文章正文
    """
    try:
        id = get_parameter(request.POST.get('id'), para_intro='文章ID', valid_check=INTEGER_NONNEGATIVE)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.get_article_by_pk(id, is_portal_view=True)}
    return utils_common.response(dict_resp)


# @require_GET
# def portal_channel_list(request):
#     """
#         获取所有可用（即已启用的）频道和栏目
#     """
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.load_hierarchical_channels()}
#     return utils.response(dict_resp)


# @require_POST
# def portal_channel_get(request):
#     try:
#         key = get_parameter(request.POST.get('key'), para_intro='关键字')
#     except InvalidParaException as ipe:
#         logger.exception(ipe)
#         return utils.response(respformat(ipe.message))
#
#     col_info = services.get_col_info_by_key(key)
#     if not col_info:
#         return utils.response(get_msg(REQUEST_PARAM_ERROR))
#
#     dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": col_info}
#     return utils.response(dict_resp)


@require_POST
def portal_article_search(request):
    """
        搜索，支持文章标题关键字，需要过滤掉不支持搜索的栏目
    """
    try:
        keyword = get_parameter(request.POST.get('key'), para_intro='文章标题关键字')
        page = get_parameter(request.POST.get('page'), para_intro='页码'
                             , valid_check=INTEGER_POSITIVE)
        rows = get_parameter(request.POST.get('rows'), para_intro='每页记录数'
                             , valid_check=INTEGER_IN_RANGE, min=1, max=50)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    #keyword = urllib2.unquote(keyword).decode('')#.encode()
    #print services.find_articles_by_keyword(keyword).count()

    # 获取所有符合条件的文章
    pager = Paginator(services.find_articles_by_keyword(keyword), int(rows))

    if int(page) > int(pager.num_pages):
        return utils_common.response(get_msg(ARTICLE_PAGER_OUT_OF_INDEX))

    range_records = pager.page(page)
    rows = list()
    for each_record in range_records:
        rows.append({
            'id': str(each_record.id),
            'title': each_record.title,
            'publish_user_id': each_record.publish_user.id,
            'publish_user_name': each_record.publish_user.name,
            'intro': each_record.intro,
            'image': services.get_article_cover(each_record),
            'click': str(each_record.click),
            'publish_time': utils_common.datetime2str(each_record.publish_time),
            # 'category_id': each_record.category.id,
            # 'name': each_record.category.name,
            # 'category_key': each_record.category.key,
            # 'category_type_id': each_record.category.type.id,
            'is_new': utils_common.bool2str(services.is_new_article(each_record.publish_time)),
            'expert_id': each_record.expert.id if each_record.expert else '',
            'expert_name': each_record.expert.expert_name if each_record.expert else '',
            'author': each_record.author,
        })

    result = {
        'page': page,
        'total': pager.num_pages,
        'records': pager.count,
        'rows': rows
    }

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": result}
    return utils_common.response(dict_resp)


@require_POST
def portal_article_list(request):
    """
        获取一个频道/栏目/推送栏目下面的所有文章，这些文章需要是审核通过的（该接口需要分页）
    """
    try:
        page = get_parameter(request.POST.get('page'), para_intro='页码'
                             , valid_check=INTEGER_POSITIVE)
        rows = get_parameter(request.POST.get('rows'), para_intro='每页记录数'
                             , valid_check=INTEGER_IN_RANGE, min=1, max=50)
    except InvalidParaException as ipe:
        return utils_common.response(respformat(ipe.message))

    pager = Paginator(services.load_all_article(), int(rows))

    if int(page) > int(pager.num_pages):
        return utils_common.response(get_msg(ARTICLE_PAGER_OUT_OF_INDEX))

    range_records = pager.page(page)
    rows = list()
    for each_record in range_records:
        rows.append({
            'id': str(each_record.id),
            'title': each_record.title,
            'publish_user_id': each_record.publish_user.id,
            'publish_user_name': each_record.publish_user.name,
            'intro': each_record.intro,
            'image': services.get_article_cover(each_record),
            'click': str(each_record.click),
            'publish_time': utils_common.datetime2str(each_record.publish_time),
            'is_new': utils_common.bool2str(services.is_new_article(each_record.publish_time)),
            'is_top': utils_common.bool2str(each_record.is_top),
            'author': each_record.author,
            'expert_id': each_record.expert.id if each_record.expert else '',
            'expert_name': each_record.expert.expert_name if each_record.expert else '',
        })

    result = {
        'page': page,
        'total': pager.num_pages,
        'records': pager.count,
        'rows': rows,
    }

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": result}
    return utils_common.response(dict_resp)













# def edit_description_view(request):
#
#     # file_path1 = 'article/image/%(basename)s_%(datetime)s.%(extname)s'
#     # file_path2 = 'article/file/%(basename)s_%(datetime)s.%(extname)s'
#     file_path1 = '1/'
#     file_path2 = file_path1
#
#     form = TestUEditorForm()
#     form.fields['Description'].widget._upload_settings['imagePathFormat'] = file_path1
#     form.fields['Description'].widget._upload_settings['filePathFormat'] = file_path2
#     return render(request,'edit-description.htm',{"form": form})


