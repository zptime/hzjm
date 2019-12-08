# -*- coding: utf-8 -*-
import HTMLParser
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from app_site.forms import CommonUeditorForm, PhotoUeditorForm
from utils import utils_common
from utils.err_code import *
from utils.para_check import *
from app_site.models import *
from utils.utils_common import require_roles, respformat

logger = logging.getLogger(__name__)


DEFAULT_LIST_PAGE = 'portal/list.html'
DEFAULT_CONTENT_PAGE = 'portal/content.html'


@require_GET
def portal_index(request):
    """
        进入门户首页
    """
    return render(request, 'portal/list.html')


@require_GET
def portal_search(request):
    """
        进入搜索页面
    """
    try:
        searchkey = get_parameter(request.GET.get('searchkey'), para_intro='查询关键字（文章标题模糊查询）')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))
    return render(request, 'portal/find.html', {'searchkey': searchkey})


# @require_GET
# def portal_quickfunc(request):
#     """
#         进入快速功能导航页面
#     """
#     return render(request, 'portal/quickfunc.html', {})


@require_GET
def portal_content(request):
    """
        进入文章正文页面
    """
    try:
        articleid = get_parameter(request.GET.get('articleid'), para_intro='文章ID编号')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    # 检查文章编号是否合法
    article_qs = SiteArticle.objects.filter(is_delete=False, id=articleid)
    if not article_qs.exists():
        utils_common.response(get_msg(ARTICLE_ID_INVALID))

    this_article = article_qs.first()

    page_goto = DEFAULT_CONTENT_PAGE

    ctx = {'article_id': articleid}
    return render(request, page_goto, ctx)


@require_GET
def portal_article_list(request):
    """
        进入某一个栏目的文章列表页面
        page/hzjm/article/list
    """
    try:
        column = get_parameter(request.GET.get('columnkey'), para_intro='栏目/频道/推送频道关键字')
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    ctx = {'channel_key': '', 'category_key': '', 'article_id': ''}

    category = SiteCategory.objects.filter(is_delete=False, is_active=True, key=column, link='').first()
    channel = SiteChannel.objects.filter(is_delete=False, is_active=True, key=column, link='').first()
    push_channel = SitePushChannel.objects.filter(is_delete=False, is_active=True, key=column).first()

    # 如果请求的是栏目
    if category:
        ctx['category_key'] = category.key
        ctx['channel_key'] = category.channel.key
        page_goto = category.type.page_list or DEFAULT_LIST_PAGE
        if category.type.is_allow_direct and category.is_support_direct:  # 支持单文直达
            articles_qs = SiteArticle.objects.filter(is_delete=False, category=category)
            if articles_qs.count() == 1:
                ctx['article_id'] = articles_qs.first().id
                page_goto = category.type.page_content or DEFAULT_CONTENT_PAGE

    # 如果请求的是频道
    elif channel:
        default_cate = SiteCategory.objects.filter(channel=channel, link='', is_default=True, is_delete=False, is_active=True).first()
        if not default_cate:
            default_cate = SiteCategory.objects.filter(channel=channel, link='', is_delete=False, is_active=True).first()
        if not default_cate:
            #return utils.response(get_msg(CHANNEL_NOT_HAS_CATEGORY))
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        ctx['category_key'] = default_cate.key
        ctx['channel_key'] = default_cate.channel.key
        page_goto = default_cate.type.page_list or DEFAULT_LIST_PAGE
        if default_cate.type.is_allow_direct and default_cate.is_support_direct:  # 支持单文直达
            articles_qs = SiteArticle.objects.filter(is_delete=False, category=default_cate)
            if articles_qs.count() == 1:
                ctx['article_id'] = articles_qs.first().id
                page_goto = default_cate.type.page_content or DEFAULT_CONTENT_PAGE

    # 如果请求的是一个推送频道
    elif push_channel:
        ctx['channel_key'] = push_channel.key
        page_goto = 'hzjm/list_push.html'
    else:
        return utils_common.response(get_msg(CHANNEL_NOT_EXIST))
    return render(request, page_goto, ctx)


@require_GET
def portal_expert(request):
    """
        进入门户首页
    """
    return render(request, 'portal/expert.html')

@require_GET
def portal_expert_content(request):
    """
        进入门户首页
    """
    return render(request, 'portal/expert_content.html')


@require_GET
def manage_login(request):
    return render(request, 'manage/login.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def page_upload(request):
    return render(request, 'manage/upload.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_article(request):
    return render(request, 'manage/manage_article.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_expert(request):
    return render(request, 'manage/manage_expert.html', {})

@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def expert_edit(request):
    return render(request, 'manage/expert_edit.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def expert_preview(request):
    return render(request, 'manage/expert_preview.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER,))
def manage_article_teacher(request):
    return render(request, 'manage/manage_mine.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_article_push(request):
    return render(request, 'manage/manage_article_push.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_pendlist(request):
    return render(request, 'manage/manage_pend.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_user(request):
    return render(request, 'manage/manage_user.html', {})


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_component(request):
#     return render(request, 'manage/manage_component.html', {})


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_picture(request):
#     return render(request, 'manage/manage_picture.html', {})


# @require_GET
# def manage_quickfunc(request):
#     return render(request, 'manage/manage_quickfunc.html', {})


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel(request):
#     return render(request, 'manage/manage_channel.html', {})


# @require_GET
# @login_required
# @require_roles(allow=(DB_USER_ROLE_ADMIN,))
# def manage_channel_push(request):
#     return render(request, 'manage/manage_channel_push.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_preview(request):
    """
        进入文章预览页面
        page/manage/preview
    """
    try:
        is_preview = get_parameter(request.GET.get('is_preview'), para_intro='是否预览', allow_null=True, default=FALSE,
                                   valid_check=CHOICES, choices=(TRUE, FALSE))
        if is_preview == FALSE:
            articleid = get_parameter(request.GET.get('articleid'), para_intro='文章ID编号', valid_check=INTEGER_NONNEGATIVE)
        else:
            articleid = ''
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    if is_preview == FALSE:
        article = SiteArticle.objects.filter(is_delete=False, id=articleid).first()
    else:
        article = SiteArticle.objects.filter(author__startswith='preview_' + str(request.user.id) + '_', is_delete=True).first()
    if not article:
        return utils_common.response(get_msg(ARTICLE_ID_INVALID))

    return render(request, 'manage/manage_preview.html', {'article_id': articleid})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER,))
def manage_mine(request):
    return render(request, 'manage/manage_mine.html', {})


@require_GET
def manage_home(request):
    """
        未登录则显示登录界面，已登录则为不同的用户显示不同的页面
    """
    if request.user.is_anonymous():
        return render(request, 'manage/login.html', {})

    if request.user.role == DB_USER_ROLE_ADMIN:
        return render(request, 'manage/manage_article.html', {})
    elif request.user.role == DB_USER_ROLE_TEACHER:
        return render(request, 'manage/manage_mine.html', {})
    else:
        return render(request, 'manage/login.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def manage_sys(request):
    return render(request, 'manage/manage_sys.html', {})


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_TEACHER, DB_USER_ROLE_ADMIN))
def manage_draft(request):
    """
        进入文章编写页面
        page/manage/draft
    """
    try:
        articleid = get_parameter(request.GET.get('articleid'), allow_null=True, default=None, para_intro='文章ID编号', valid_check=INTEGER_NONNEGATIVE)
    except InvalidParaException as ipe:
        logger.exception(ipe)
        return utils_common.response(respformat(ipe.message))

    html_parser = HTMLParser.HTMLParser()

    #当传入栏目key时，需要将栏目ID和NAME提供给前端进行展示
    page_article_id = ''
    if articleid:  # 编辑模式
        article = SiteArticle.objects.filter(is_delete=False, id=int(articleid)).first()
        if not article:
            return utils_common.response(get_msg(ARTICLE_ID_INVALID))
        page_article_id = str(articleid)
        editorform = CommonUeditorForm({'content': html_parser.unescape(html_parser.unescape(article.content))})
    else:  # 新增模式
        editorform = CommonUeditorForm()

    tmp_img_save_location = ARTICLE_IMAGE_TEMP % datetime.now().strftime('%Y%m')
    tmp_file_save_location = ARTICLE_IMAGE_FILE % datetime.now().strftime('%Y%m')
    tmp_video_save_location = ARTICLE_VIDEO_TEMP % datetime.now().strftime('%Y%m')

    editorform.fields['content'].widget._upload_settings['imagePathFormat'] = tmp_img_save_location
    editorform.fields['content'].widget._upload_settings['filePathFormat'] = tmp_file_save_location
    editorform.fields['content'].widget._upload_settings['videoPathFormat'] = tmp_video_save_location

    return render(request, 'manage/manage_draft.html', {"form": editorform, 'article_id': page_article_id})









