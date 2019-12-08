# -*- coding: utf-8 -*-
import HTMLParser
import logging
# import datetime
import os

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction
from django.db.models import F

from app_common.models import CommonParameter
from app_site.models import *
from hzjm.settings import BASE_DIR, MEDIA_URL
from utils.err_code import *
from utils.para_check import *
from utils import utils_common
from utils.const import *
from utils.utils_common import getpages
from utils.utils_except import BusinessException

logger = logging.getLogger(__name__)


def is_cpnt_key_ref(key):
    try:
        parameter = CommonParameter.objects.get(key=HOMEPAGE_REF_CPNT_KEYS)
    except (ObjectDoesNotExist, MultipleObjectsReturned), e:
        logger.exception(e)
        return False
    return key in parameter.value1.split(',')


def is_col_key_ref(key):
    pass


# def load_occupied_column_key():
#     result_list = list()
#     for each_channel in SiteChannel.objects.filter(is_delete=False):
#         result_list.append(each_channel.key)
#     for each_category in SiteCategory.objects.filter(is_delete=False):
#         result_list.append(each_category.key)
#     for each_push_channel in SitePushChannel.objects.filter(is_delete=False):
#         result_list.append(each_push_channel.key)
#     return result_list


# def load_occupied_component_key():
#     result_list = list()
#     for each_component in SiteComponent.objects.filter(is_delete=False):
#         result_list.append(each_component.key)
#     return result_list


def is_new_article(publish_time):
    if not publish_time:
        return False
    new_pulish_time_qs = CommonParameter.objects.filter(key=NEW_PUBLISH_TIME, is_delete=False).first()
    if not new_pulish_time_qs:
        return False
    try:
        new_pulish_time_int = int(new_pulish_time_qs.value1)
    except:
        new_pulish_time_int = 3  # 如果管理员输入非数字，则默认为3天
    return (datetime.now() - publish_time).days <= new_pulish_time_int


def load_all_article(only_show_passed=True):
    """
        获取全站所有文章
    """
    qs = SiteArticle.objects.filter(is_delete=False)
    if only_show_passed:
        qs = qs.filter(admit_status=DB_ARTICLE_ADMIT_STATE_PASS)
    return qs.select_related()   #.order_by('is_top', '-publish_time', '-create_time')


def load_all_article_in_channel(channel, only_show_passed=True):
    """
        获取某一个频道的所有文章
        返回queryset
    """
    qs = SiteArticle.objects.filter(category__channel=channel, is_delete=False, category__is_active=True,
                                    category__is_delete=False)
    if only_show_passed:
        qs = qs.filter(admit_status=DB_ARTICLE_ADMIT_STATE_PASS)
    return qs.select_related()  #.order_by('-is_top', '-publish_time', '-create_time')


def find_articles_by_keyword(keyword):
    """
        依照关键字和专家进行查找文章
        返回queryset
    """
    test = repr(keyword)

    article_title = SiteArticle.objects.filter(title__icontains=keyword, admit_status=DB_ARTICLE_ADMIT_STATE_PASS, is_delete=False) \
        .order_by('-publish_time', '-create_time')
    article_expert = SiteArticle.objects.filter(expert__expert_name__contains=keyword, admit_status=DB_ARTICLE_ADMIT_STATE_PASS, is_delete=False) \
        .order_by('-publish_time', '-create_time')
    article_author = SiteArticle.objects.filter(author__contains=keyword, admit_status=DB_ARTICLE_ADMIT_STATE_PASS, is_delete=False) \
        .order_by('-publish_time', '-create_time')

    articles = (article_title | article_expert | article_author).distinct().order_by('-publish_time', '-create_time')
    return articles


def load_all_article_in_category(category, only_show_passed=True):
    """
        获取某一个栏目的所有文章
        返回queryset
    """
    qs = SiteArticle.objects.filter(category=category, is_delete=False,
                                    category__is_delete=False)
    if only_show_passed:
        qs = qs.filter(admit_status=DB_ARTICLE_ADMIT_STATE_PASS)
    return qs.select_related()  #.order_by('-is_top', '-publish_time', '-create_time')


# def load_all_article_in_push_channel(push_channel, only_show_passed=True):
#     """
#         获取某一个推送频道的所有文章
#     """
#     qs = SitePushArticle.objects.select_related().filter(push_channel=push_channel,
#                                                          push_article__category__is_delete=False).order_by(
#         '-push_article__publish_time', '-push_article__create_time', '-create_time')
#     result_list = list()
#     for each_push in qs:
#         if only_show_passed:
#             if each_push.push_article.admit_status == DB_ARTICLE_ADMIT_STATE_PASS:
#                 result_list.append(each_push.push_article)
#         else:
#             result_list.append(each_push.push_article)
#     return result_list


def get_default_article_cover():
    default_cover_qs = CommonParameter.objects.filter(key=DEFAULT_ARTICLE_PIC, is_delete=False).first()
    if not default_cover_qs:
        return ''
    return default_cover_qs.value1


def get_article_cover(article):
    """
        获取一篇文章的封面，寻找方法如下：
        优先：封面字段
        其次：正文的第一张图片（可以是内网图片，也可以是互联网上的图片）
        劣后：系统参数表中配置的文章默认封面图片
    """
    if article.image:
        if article.image.name[:4] == "http":
            return article.image.name
        else:
            return article.image.url
    try:
        re_compile = re.compile(r'src=\"(.+?\.(jpeg|jpg|gif|png|bmp))\"', re.I)
        # first_photo_url = re.search(r'src=\"(/media/article/.+?)\"', article.content).group(1)
        first_photo_url = re_compile.search(article.content).group(1)
    except:
        return get_default_article_cover()
    return first_photo_url


def get_pre_article(article, only_show_admit=True, key=None):
    # if key:
    #     key_push_cnt = SitePushChannel.objects.filter(key=key, is_delete=False).count()
    #     if key_push_cnt > 0 :
    #         article_create_time = SitePushArticle.objects.filter(push_article=article).first().create_time
    # else:
    #     key_push_cnt = 0

    # if key_push_cnt == 0:
    pre_article_qs = SiteArticle.objects.filter(is_delete=False,\
                            publish_time__gt=article.publish_time).order_by('publish_time', 'create_time')
    if only_show_admit is True:
        pre_article_qs = pre_article_qs.filter(admit_status=DB_ARTICLE_ADMIT_STATE_PASS)
    pre_article = pre_article_qs.first()
    # else:
    #     if only_show_admit is True:
    #         pre_push_article_qs = SitePushArticle.objects.filter(push_channel__key=key, push_article__publish_time__gt=article.publish_time, push_article__is_delete=False,
    #                                                              push_article__admit_status=DB_ARTICLE_ADMIT_STATE_PASS).order_by(
    #             'push_article__publish_time', 'create_time', 'push_article__create_time').first()
    #     else:
    #         pre_push_article_qs = SitePushArticle.objects.filter(push_channel__key=key, push_article__is_delete=False,
    #                                                              push_article__publish_time__gt=article.publish_time).order_by(
    #             'push_article__publish_time', 'create_time', 'push_article__create_time').first()
    #     if pre_push_article_qs:
    #         pre_article = pre_push_article_qs.push_article
    #     else:
    #         pre_article = None

    return pre_article


def get_next_article(article, only_show_admit=True, key=None):
    next_article_qs = SiteArticle.objects.filter(is_delete=False,\
                            publish_time__lt=article.publish_time).order_by('-publish_time', '-create_time')
    if only_show_admit is True:
        next_article_qs = next_article_qs.filter(admit_status=DB_ARTICLE_ADMIT_STATE_PASS)
    next_article = next_article_qs.first()

    return next_article


# def load_category_types():
#     category_list_qs = SiteCategoryType.objects.filter(is_delete=False)
#     category_list = list()
#     for each_cate_type in category_list_qs:
#         image_url = ''
#         if each_cate_type.image:
#             image_url = each_cate_type.image.url
#         category_list.append({
#             'id': str(each_cate_type.id),
#             'key': each_cate_type.key,
#             'name': each_cate_type.name,
#             'image': image_url
#         })
#     return category_list

#
# def load_push_channels(only_show_active=False):
#     push_channel_qs = SitePushChannel.objects.filter(is_delete=False)
#     if only_show_active:
#         push_channel_qs = push_channel_qs.filter(is_active=True)
#     push_channel_list = list()
#     for each_push_channel in push_channel_qs:
#         article_count = SitePushArticle.objects.filter(push_channel=each_push_channel).count()
#         push_channel_list.append({
#             'id': str(each_push_channel.id),
#             'key': each_push_channel.key,
#             'name': each_push_channel.name,
#             'is_active': utils.bool2str(each_push_channel.is_active),
#             'article_count': str(article_count)
#         })
#     return push_channel_list
#
#
# def load_categorys(channel, only_show_on_navi=False, only_show_active=False):
#     category_qs = SiteCategory.objects.filter(channel=channel, is_delete=False).order_by('sort', 'create_time')
#     if only_show_on_navi:
#         category_qs = category_qs.filter(is_navi_show=True)
#     if only_show_active:
#         category_qs = category_qs.filter(only_show_active=True)
#     category_list = list()
#     for each_category in category_qs:
#         article_count = SiteArticle.objects.filter(category=each_category, is_delete=False).count()
#         category = {
#             'id': str(each_category.id),
#             'key': each_category.key,
#             'name': each_category.name,
#             'link': each_category.link or '',
#             'sort': str(each_category.sort),
#             'is_link_out_open': utils.bool2str(each_category.is_link_out_open),
#             'is_active': utils.bool2str(each_category.is_active),
#             'is_navi_show': utils.bool2str(each_category.is_navi_show),
#             'type_id': each_category.type.id,
#             'type_name': each_category.type.name,
#             'channel_id': each_category.channel.id,
#             'channel_name': each_category.channel.name,
#             'is_support_direct': utils.bool2str(each_category.is_support_direct),
#             'is_default': utils.bool2str(each_category.is_default),
#             'article_count': str(article_count)
#         }
#         category_list.append(category)
#     return category_list
#
#
# def load_channels(only_show_on_navi=False, only_show_active=False):
#     """
#         获取频道列表
#     """
#     channels_qs = SiteChannel.objects.filter(is_delete=False).exclude(key='chan_xnzy').order_by('sort', 'create_time')
#     if only_show_active:
#         channels_qs = channels_qs.filter(is_active=True)
#     if only_show_on_navi:
#         channels_qs = channels_qs.filter(is_navi_show=True)
#     channel_list = list()
#     for each_channel in channels_qs:
#         article_count = SiteArticle.objects.filter(is_delete=False, category__channel=each_channel).count()
#         channel = {
#             'id': str(each_channel.id),
#             'key': each_channel.key,
#             'name': each_channel.name,
#             'link': each_channel.link or '',
#             'sort': str(each_channel.sort),
#             'is_link_out_open': utils.bool2str(each_channel.is_link_out_open),
#             'is_active': utils.bool2str(each_channel.is_active),
#             'is_navi_show': utils.bool2str(each_channel.is_navi_show),
#             'article_count': str(article_count)
#         }
#         channel_list.append(channel)
#     return channel_list

#
# def load_components():
#     components_qs = SiteComponent.objects.filter(is_delete=False)
#     component_list = list()
#     for each_component in components_qs:
#         image_url = ''
#         if each_component.image:
#             image_url = each_component.image.url
#         component_list.append({
#             'id': str(each_component.id),
#             'key': each_component.key,
#             'name': each_component.name,
#             'intro': each_component.intro,
#             'image': image_url,
#             'link': each_component.link,
#             'is_link_out_open': utils.bool2str(each_component.is_link_out_open),
#         })
#     return component_list


# def get_col_info_by_key(key, only_show_active=False):
#     categorys_qs = SiteCategory.objects.filter(key=key, is_delete=False)
#     if only_show_active:
#         categorys_qs = categorys_qs.filter(is_active=True)
#     channels_qs = SiteChannel.objects.filter(key=key, is_delete=False)
#     if only_show_active:
#         channels_qs = channels_qs.filter(is_active=True)
#     push_channels_qs = SitePushChannel.objects.filter(key=key, is_delete=False)
#     if only_show_active:
#         push_channels_qs = push_channels_qs.filter(is_active=True)
#
#     if categorys_qs.exists():
#         cate = categorys_qs.first()
#         id = cate.id
#         name = cate.name
#         key = cate.key
#         key_type = CODE_CATEGORY
#     elif channels_qs.exists():
#         chan = channels_qs.first()
#         id = chan.id
#         name = chan.name
#         key = chan.key
#         key_type = CODE_CHANNEL
#     elif push_channels_qs.exists():
#         push_chan = push_channels_qs.first()
#         id = push_chan.id
#         name = push_chan.name
#         key = push_chan.key
#         key_type = CODE_PUSH_CHANNEL
#     else:
#         return None
#
#     return {
#         'id': str(id),
#         'name': name,
#         'key': key,
#         'key_type': key_type
#     }


# def load_hierarchical_channels(only_show_active=True, user=None):
#     """
#         获取频道和栏目
#     """
#     channels_qs = SiteChannel.objects.filter(is_delete=False).order_by('sort', 'create_time')
#     if only_show_active:
#         channels_qs = channels_qs.filter(is_active=True)
#
#     channel_list = list()
#     for each_channel in channels_qs:
#         category_qs = SiteCategory.objects.filter(channel=each_channel, is_delete=False).order_by('sort', 'create_time')
#         if only_show_active:
#             category_qs = category_qs.filter(is_active=True)
#         category_list = list()
#         for each_category in category_qs:
#             if user:
#                 article_count_category = SiteArticle.objects.filter(is_delete=False, category=each_category, publish_user=user).count()
#             else:
#                 article_count_category = SiteArticle.objects.filter(is_delete=False, category=each_category).count()
#             category_list.append({
#                 'id': str(each_category.id),
#                 'key': each_category.key,
#                 'name': each_category.name,
#                 'sort': str(each_category.sort),
#                 'type_id': str(each_category.type.id),
#                 'link': each_category.link or '',
#                 'is_navi_show': utils.bool2str(each_category.is_navi_show),
#                 'is_link_out_open': utils.bool2str(each_category.is_link_out_open),
#                 'article_count': str(article_count_category),
#                 'is_active': utils.bool2str(each_category.is_active),
#                 'is_support_direct': utils.bool2str(each_category.is_support_direct),
#             })
#         if user:
#             article_count_channel = SiteArticle.objects.filter(is_delete=False, category__channel=each_channel, publish_user=user).count()
#         else:
#             article_count_channel = SiteArticle.objects.filter(is_delete=False, category__channel=each_channel).count()
#         channel = {
#             'id': str(each_channel.id),
#             'key': each_channel.key,
#             'name': each_channel.name,
#             'sort': str(each_channel.sort),
#             'link': each_channel.link or '',
#             'is_link_out_open': utils.bool2str(each_channel.is_link_out_open),
#             'is_navi_show': utils.bool2str(each_channel.is_navi_show),
#             'category_list': category_list,
#             'article_count': str(article_count_channel),
#             'is_active': utils.bool2str(each_channel.is_active)
#         }
#         channel_list.append(channel)
#     return channel_list


# def load_quickfunc(only_show_active=True):
#     quickfunc_list_qs = SiteQuickFunc.objects.filter(is_delete=False).order_by('sort')
#     if only_show_active:
#         quickfunc_list_qs = quickfunc_list_qs.filter(is_active=True)
#     quickfunc_list = list()
#     for each_quickfunc in quickfunc_list_qs:
#         image_url = ''
#         if each_quickfunc.image:
#             image_url = each_quickfunc.image.url
#         quickfunc_list.append({
#             'id': str(each_quickfunc.id),
#             'name': each_quickfunc.name,
#             'intro': each_quickfunc.intro or '',
#             'sort': str(each_quickfunc.sort),
#             'image': image_url,
#             'link': each_quickfunc.link or '',
#             'is_link_out_open': utils.bool2str(each_quickfunc.is_link_out_open),
#             'is_active': utils.bool2str(each_quickfunc.is_active),
#         })
#     return quickfunc_list


def get_article_by_pk(pk, is_portal_view=False, key=None):
    """
        通过文章ID获得文章正文
    """
    article_qs = SiteArticle.objects.filter(pk=pk, is_delete=False)
    if is_portal_view:
        article_qs = article_qs.filter(admit_status=DB_ARTICLE_ADMIT_STATE_PASS)

    article = article_qs.first()
    if not article:
        return ARTICLE_ID_INVALID[1]
        # return utils.response(get_msg(ARTICLE_ID_INVALID))

    current_click_count = str(article.click)
    # 如果是客户从门户访问文章，文章统计数量+1
    if is_portal_view:
        current_click_count = str(article.click + 1)
        article.click = F('click') + 1
        article.save()

    if not article.admit_user:
        admit_user_id = ''
        admit_user_name = ''
    else:
        admit_user_id = str(article.admit_user.id)
        admit_user_name = article.admit_user.name

    # 找到本篇文章的上一篇文章和下一篇文章
    pre_article = get_pre_article(article, key=key)
    if not pre_article:
        pre_article_id = ''
        pre_article_title = ''
    else:
        pre_article_id = pre_article.id
        pre_article_title = pre_article.title
    next_article = get_next_article(article, key=key)
    if not next_article:
        next_article_id = ''
        next_article_title = ''
    else:
        next_article_id = next_article.id
        next_article_title = next_article.title

    html_parser = HTMLParser.HTMLParser()

    # 获取pdf页数，通过读取文件最大序号实现
    if os.path.exists(BASE_DIR + r'/media/journal/swf/' + str(article.id)):
        pdftotalpages = len(os.listdir(BASE_DIR + r'/media/journal/swf/' + str(article.id)))
    else:
        pdftotalpages = 0

    return {
        'id': str(article.id),
        'content': html_parser.unescape(article.content) or '',
        'title': article.title or '',
        'subtitle': article.subtitle or '',
        'publish_user_id': str(article.publish_user.id),
        'publish_user_name': article.publish_user.name or '',
        'publish_time': utils_common.datetime2str(article.publish_time) or '',
        'image': get_article_cover(article),
        'intro': article.intro or '',
        'click': current_click_count,
        'admit_state': str(article.admit_status),
        'admit_user_id': admit_user_id,
        'admit_user_name': admit_user_name,
        'admit_time': utils_common.datetime2str(article.admit_time),
        'is_top': utils_common.bool2str(article.is_top),
        'pre_article_id': pre_article_id,
        'pre_article_title': pre_article_title,
        'next_article_id': next_article_id,
        'next_article_title': next_article_title,
        'author': article.author,
        'pdftotalpages': str(pdftotalpages),
        'video_upload_id': str(article.video_id) if article.video_id else '',
        'video_path': str(os.path.join(MEDIA_URL, article.video.url)) if article.video else '',
        'expert_id': str(article.expert_id) if article.expert_id else '',
        'expert_name': str(article.expert.expert_name) if article.expert else '',
    }


def get_article_preview_by_user(user):
    """
        通过文章ID获得文章正文
    """
    article_qs = SiteArticle.objects.filter(author__startswith='preview_' + str(user.id) + '_', is_delete=True)

    article = article_qs.first()
    if not article:
        return utils_common.response(get_msg(ARTICLE_ID_INVALID))

    if not article.admit_user:
        admit_user_id = ''
        admit_user_name = ''
    else:
        admit_user_id = str(article.admit_user.id)
        admit_user_name = article.admit_user.name

    html_parser = HTMLParser.HTMLParser()

    # 获取pdf页数，通过读取文件最大序号实现
    if os.path.exists(BASE_DIR + r'/media/journal/swf/' + str(article.id)):
        pdftotalpages = len(os.listdir(BASE_DIR + r'/media/journal/swf/' + str(article.id)))
    else:
        pdftotalpages = 0

    return {
        'id': str(article.id),
        'content': html_parser.unescape(article.content) or '',
        # 'channel_id': str(article.category.channel.id),
        # 'channel_name': article.category.channel.name,
        # 'category_id': str(article.category.id),
        # 'category_name': article.category.name,
        'title': article.title or '',
        'subtitle': article.subtitle or '',
        'publish_user_id': str(article.publish_user.id),
        'publish_user_name': article.publish_user.name or '',
        'publish_time': utils_common.datetime2str(article.publish_time) or '',
        'image': get_article_cover(article),
        'video_upload_id': str(article.video_id) if article.video_id else '',
        'video_path': str(os.path.join(MEDIA_URL, article.video.url)) if article.video else '',
        'intro': article.intro or '',
        'click': '0',
        'admit_state': str(article.admit_status),
        'admit_user_id': admit_user_id,
        'admit_user_name': admit_user_name,
        'admit_time': utils_common.datetime2str(article.admit_time),
        'is_top': utils_common.bool2str(article.is_top),
        'pre_article_id': '',
        'pre_article_title': '',
        'next_article_id': '',
        'next_article_title': '',
        # 'is_push_show_cover': utils.bool2str(article.is_push_show_cover),
        'author': article.author.replace("preview_" + str(user.id) + "_",""),
        'pdftotalpages': str(pdftotalpages),
        'expert_id': str(article.expert_id) if article.expert_id else '',
        'expert_name': str(article.expert.expert_name) if article.expert else '',
    }

#
# def load_all_picture():
#     """
#         获取所有的轮播图
#     """
#     pictures_qs = SitePicture.objects.filter(is_delete=False)
#     pictures = list()
#     for each_picture_qs in pictures_qs:
#         pictures.append({
#             'id': each_picture_qs.id,
#             'title': each_picture_qs.title,
#             'intro': each_picture_qs.intro,
#             'sort': str(each_picture_qs.sort),
#             'image': each_picture_qs.image.url,
#             'link': each_picture_qs.link,
#             'is_link_out_open': utils.bool2str(each_picture_qs.is_link_out_open)
#         })
#     return pictures


# def get_component_by_key(key):
#     """
#         通过关键字获取一个基础组件，找不到则返回None
#     """
#     components_qs = SiteComponent.objects.filter(is_delete=False, key=key)  # 大小写不敏感
#     if not components_qs.exists():
#         return None
#     this_component = components_qs.first()
#     image_url = ''
#     if this_component.image:
#         image_url = this_component.image.url
#     return {
#         'id': str(this_component.id),
#         'key': this_component.key,
#         'name': this_component.name,
#         'intro': this_component.intro or '',
#         'image': image_url,
#         'link': this_component.link  or '',
#         'is_link_out_open': utils.bool2str(this_component.is_link_out_open),
#     }
def manage_expert_add(expert_name, expert_sortorder, expert_image, expert_intro):
    if not expert_sortorder:
        expert_sortorder = '100'

    expert = SiteExpert()
    expert.expert_name = expert_name
    expert.image_url = expert_image
    expert.article_num = 0
    expert.expert_intro = expert_intro
    expert.sort_order = expert_sortorder
    expert.save()

    result = {
        "expert_id": expert.id,
        "expert_name": expert.expert_name,
        "expert_sortorder": expert.sort_order,
        "expert_article_num": expert.article_num,
        "expert_image": expert.image_url.url if expert.image_url else '',
        "expert_intro": expert.expert_intro,
    }
    return result


def manage_expert_delete(id_list):
    ids = id_list.rstrip(',').split(',')
    # 先检查专家文章数量，如果文章数量不为0则不允许删除
    for each_expertid in ids:
        expert = SiteExpert.objects.get(id=each_expertid)
        if expert.article_num != 0:
            raise BusinessException(EXPERT_HAS_ARTICLE)
    SiteExpert.objects.filter(id__in=ids).update(is_delete=TRUE_INT)
    return 'OK'


def manage_expert_edit(expert_id, expert_name, expert_sortorder, expert_image, expert_intro):
    if not expert_sortorder:
        expert_sortorder = '100'

    expert = SiteExpert.objects.get(id=expert_id, is_delete=FALSE_INT)
    expert.expert_name = expert_name
    if expert_image:
        expert.image_url = expert_image
    # expert.article_num = 0
    expert.expert_intro = expert_intro
    expert.sort_order = expert_sortorder
    expert.save()

    expert_articlenum_update(expert_id)

    result = {
        "expert_id": expert.id,
        "expert_name": expert.expert_name,
        "expert_sortorder": expert.sort_order,
        "expert_article_num": expert.article_num,
        "expert_image": expert.image_url.url if expert.image_url else '',
        "expert_intro": expert.expert_intro,
    }
    return result


def manage_expert_get(expert_id):
    expert = SiteExpert.objects.get(id=expert_id, is_delete=FALSE_INT)
    result = {
        "expert_id": expert.id,
        "expert_name": expert.expert_name,
        "expert_sortorder": expert.sort_order,
        "expert_article_num": expert.article_num,
        "expert_image": expert.image_url.url if expert.image_url else '',
        "expert_intro": expert.expert_intro,
    }
    return result


def manage_expert_list(key, page, rows):
    result = dict()
    experts = SiteExpert.objects.filter(expert_name__contains=key, is_delete=FALSE_INT).order_by('sort_order')

    cnt = experts.count()  # 总数量
    if rows:
        num_pages, cur_start, cur_end = getpages(cnt, page, rows)
        expert_cycle = experts[cur_start:cur_end]
    else:
        page = 1
        rows = cnt
        num_pages = 1
        cur_start = 1
        cur_end = cnt
        expert_cycle = experts

    result['cur_page'] = page
    result['max_page'] = num_pages
    result['total'] = cnt

    expert_list = list()
    for each_expert in expert_cycle:
        expert_dict = {
            "expert_id": each_expert.id,
            "expert_name": each_expert.expert_name,
            "expert_sortorder": each_expert.sort_order,
            "expert_article_num": each_expert.article_num,
            "expert_image": each_expert.image_url.url if each_expert.image_url else '',
            "expert_intro": each_expert.expert_intro,
        }
        expert_list.append(expert_dict)
    result['expert_list'] = expert_list
    return result


def expert_articlenum_update(expert_id):
    # 重新计算单个专家的文章数
    if not expert_id:
        return 0

    article_num = SiteArticle.objects.filter(expert_id=expert_id, is_delete=FALSE_INT).count()
    SiteExpert.objects.filter(id=expert_id, is_delete=FALSE_INT).update(article_num=article_num)
    return article_num
