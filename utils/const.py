# -*- coding: utf-8 -*-

# 是/否
import json

from django.http import HttpResponse

TRUE = '1'
FALSE = '0'

TRUE_INT = 1
FALSE_INT = 0

CHANNEL_SORT_DEFAULT = '100'

# 图片/文件/附件 存储位置

PROPAGANDA_PIC = 'propaganda/'  # 轮播宣传图

CATELORY_TITLE_PIC = 'catelory/title'  # 栏目的题图图片存放位置
CATELORY_TYPE_INTRO_PIC = 'catelory/type_intro'  # 栏目的类型介绍图片存放位置

COMPONENT_PIC = 'component/pic'  # 基本组件配图存放位置
QUICKFUNC_PIC = 'quickfunc'  # 快速功能配图存放位置

ARTICLE_COVER = 'article/%s/cover/%s'  # 文章封面 (article/年份月份/cover/文件名)
ARTICLE_IMAGE = 'article/%s/image/'  # 文章图片 (article/年份月份/image/)
ARTICLE_FILE = 'article/%s/file/'  # 文章附件 (article/年份月份/file/)
ARTICLE_VIDEO = 'article/%s/video/'  # 文章视频 (article/年份月份/video/)

ARTICLE_IMAGE_TEMP = 'temp/%s/image/'  # 文章图片暂存
ARTICLE_IMAGE_FILE = 'temp/%s/file/'   # 文章附件暂存
ARTICLE_VIDEO_TEMP = 'temp/%s/video/'   # 视频附件暂存

EXPERT_IMAGE = 'expert/image/%s'  # 专家头像

TEMP_IMAGE = 'temp/images/'  # 临时图片存放地址


# 不同级别栏目静态定义常量
# IS_A_CHANNEL = '0'
# IS_A_CATEGORY = '1'
# IS_A_PUSH_CHANNEL = '9'


# 系统参数常量表
NEW_PUBLISH_TIME = 'new_publish_time'
DEFAULT_ARTICLE_PIC = 'default_article_pic'
HOMEPAGE_REF_CPNT_KEYS = 'homepage_ref_cpnt_keys'
HOMEPAGE_REF_COL_KEYS = 'homepage_ref_col_keys'


CODE_CHANNEL = '1'
CODE_CATEGORY = '2'
CODE_PUSH_CHANNEL = '9'


# --------------------- 数据库相关字段的静态值定义 ---------------------

DB_ARTICLE_ADMIT_STATE_PEND = 0
DB_ARTICLE_ADMIT_STATE_PASS = 1
DB_ARTICLE_ADMIT_STATE_FAIL = 2

DB_USER_ROLE_ADMIN = 0
DB_USER_ROLE_TEACHER = 1
DB_USER_ROLE_STUDENT = 2
DB_USER_ROLE_OTHER = 3

MANAGE_DRAFT_COMMON = 1
MANAGE_DRAFT_PROFILE = 2
MANAGE_DRAFT_PHOTO = 3
MANAGE_DRAFT_JOURNAL = 4

JOB_STATE_PEND = 0  # 待处理
JOB_STATE_OK = 1  # 处理成功
JOB_STATE_DEAL = 2  # 处理中
JOB_STATE_FAIL = 3  # 处理失败


def helper_const_list(request):
    data = [
        {'code': 'FALSE', 'value': '0', 'intro': u'否（用于is_xxx字段）'},
        {'code': 'TRUE', 'value': '1', 'intro': u'是（用于is_xxx字段）'},

        {'code': 'DB_ARTICLE_ADMIT_STATE_PEND', 'value':'0', 'intro': u'文章审核状态：待审核'},
        {'code': 'DB_ARTICLE_ADMIT_STATE_PASS', 'value': '1', 'intro': u'文章审核状态：已通过审核'},
        {'code': 'DB_ARTICLE_ADMIT_STATE_FAIL', 'value': '2', 'intro': u'文章审核状态：未通过审核'},

        {'code': 'DB_USER_ROLE_ADMIN', 'value': '0', 'intro': u'角色：管理员'},
        {'code': 'DB_USER_ROLE_TEACHER', 'value': '1', 'intro': u'角色：普通教师'},
        {'code': 'DB_USER_ROLE_STUDENT', 'value': '2', 'intro': u'角色：学生'},
        {'code': 'DB_USER_ROLE_OTHER', 'value': '3', 'intro': u'角色：其它'},

        {'code': 'CODE_CHANNEL', 'value': '1', 'intro': u'标识：频道（一级栏目）'},
        {'code': 'CODE_CATEGORY', 'value': '2', 'intro': u'标识：栏目（二级栏目）'},
        {'code': 'CODE_PUSH_CHANNEL', 'value': '9', 'intro': u'标识：推送频道'},

        {'code': 'MANAGE_DRAFT_COMMON', 'value': '1', 'intro': u'一般文章展示型'},
        {'code': 'MANAGE_DRAFT_PROFILE', 'value': '2', 'intro': u'人物肖像展示型'},
        {'code': 'MANAGE_DRAFT_PHOTO', 'value': '3', 'intro': u'照片墙展示型'},
        {'code': 'MANAGE_DRAFT_JOURNAL', 'value': '4', 'intro': u'刊物展示型'},

        {'code': 'JOB_STATE_PEND', 'value': '0', 'intro': u'待处理'},
        {'code': 'JOB_STATE_OK', 'value': '1', 'intro': u'处理成功'},
        {'code': 'JOB_STATE_DEAL', 'value': '2', 'intro': u'处理中'},
        {'code': 'JOB_STATE_FAIL', 'value': '3', 'intro': u'处理失败'},
    ]
    dict_resp = {"c": 0, "m": u'请求完成', "d": data}
    return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")