# -*- coding=utf-8 -*-

import json
from django.http import HttpResponse

REQUEST_SUCCESS = [0, u'请求完成']

REQUEST_PARAM_ERROR = [1000, u'请求参数错误']

LOGIN_WRONG_ACCOUNT = [2000, u'用户名或密码错误，或者此用户已被禁用']
LOGIN_NO_PRIVILEGES = [2001, u'权限不足，只有门户管理员和教师才可以使用本系统']
USER_DUPLICATE_ACCOUNT = [2002, u'用户名重复']
USER_NOT_EXIST = [2003, u'用户名不存在']
USER_OLD_PASSWORD_WRONG= [2004, u'原密码错误']
USER_HAS_ARTICLE= [2005, u'用户发布过文章，不能删除']

COMPONENT_NOT_FOUND = [3000, u'找不到对应组件']
COMPONENT_OCCUPIED_KEY = [3001, u'组件关键字重复，以下关键字不可重复使用： %s']
COMPONENT_REF_BY_HOMEPAGE = [3002, u'该组件被门户首页引用，不能修改引用关键字或删除']

CHANNEL_NOT_EXIST = [4000, u'频道或栏目不存在或者未启用']
CHANNEL_NOT_HAS_CATEGORY = [4001, u'该频道下没有可用栏目']
CHANNEL_INVALID = [4002, u'无效的频道']
CHANNEL_CATEGORY_INVALID = [4003, u'无效的栏目']
CHANNEL_PUSH_INVALID = [4004, u'无效的推送栏目']
CHANNEL_CATEGORY_TYPE_INVALID = [4005, u'无效的栏目类型']
CHANNEL_OCCUPIED_KEY = [4006, u'频道或栏目关键字重复，以下关键字不可重复使用： %s']
CHANNEL_CATEGORY_TYPE_CANNOT_CHANGE = [4007, u'该栏目下有文章，不可更换栏目类型']
CHANNEL_CATEGORY_CANNOT_DELETE = [4008, u'该栏目下有文章，不可删除栏目']
CHANNEL_CATEGORY_DIRECT_CONFLICT= [4009, u'该类型的栏目不可设为单文直达']
CHANNEL_WRITE_FILE_FAIL= [4010, u'PDF文件写入失败']
CHANNEL_WRITE_FILE_ERRFILE= [4012, u'错误的文件类型']

ARTICLE_PAGER_OUT_OF_INDEX = [5000, u'查询无数据']
ARTICLE_ID_INVALID = [5001, u'无效的文章编号']
ARTICLE_DIFFERENT_CATE_TYPE = [5002, u'不可将文章同时发到不同类型的栏目中']
ARTICLE_CANNOT_CHANGE_CATE_TYPE = [5003, u'不可将文章修改到不同类型的栏目中']
ARTICLE_PASS_CANNOT_DELETE = [5004, u'教师不能删除已经审批通过文章']
ARTICLE_TEACHER_ONLY_CAN_DELETE_SELF = [5005, u'教师不能删除他人发布的文章']
ARTICLE_PASS_CANNOT_MODI = [5006, u'教师不能修改已经审批通过文章']
ARTICLE_JOURNAL_UPLOAD_FAIL = [5007, u'刊物上传失败']

COMMON_SYS_PARA_NOT_EXIST= [6000, u'系统参数不存在']

QUICKFUNC_ID_INVALID = [7000, u'无效的快速功能链接ID编号']

PICTURE_ID_INVALID = [8000, u'无效的轮播图ID编号']
PICTURE_NOPIC = [8001, u'请上传图片']
PICTURE_SAVE_FAIL = [8002, u'保存轮播图失败']

EXPERT_HAS_ARTICLE = [9001, u'专家发布过文章，不允许删除']


def helper_errcode_list(request):
    data = [
        {'code': 'REQUEST_SUCCESS', 'value':'0', 'intro': u'请求完成'},

        {'code': 'REQUEST_PARAM_ERROR', 'value': '1000', 'intro': u'请求参数错误'},

        {'code': 'LOGIN_WRONG_ACCOUNT', 'value': '2000', 'intro': u'用户名或密码错误，或者此用户已被禁用'},
        {'code': 'LOGIN_NO_PRIVILEGES', 'value': '2001', 'intro': u'权限不足，只有门户管理员和教师才可以使用本系统'},
        {'code': 'USER_DUPLICATE_ACCOUNT', 'value': '2002', 'intro': u'用户名重复'},
        {'code': 'USER_NOT_EXIST', 'value': '2003', 'intro': u'用户名不存在'},
        {'code': 'USER_OLD_PASSWORD_WRONG', 'value': '2004', 'intro': u'原密码错误'},
        {'code': 'USER_HAS_ARTICLE', 'value': '2005', 'intro': u'用户发布过文章，不能删除'},

        {'code': 'COMPONENT_NOT_FOUND', 'value': '3000', 'intro': u'找不到对应组件'},
        {'code': 'COMPONENT_OCCUPIED_KEY', 'value': '3001', 'intro': u'组件关键字重复'},
        {'code': 'COMPONENT_REF_BY_HOMEPAGE', 'value': '3002', 'intro': u'该组件被门户首页引用，不能修改引用关键字或删除'},

        {'code': 'CHANNEL_NOT_ACTIVE', 'value': '4000', 'intro': u'频道或栏目不存在或者未启用'},
        {'code': 'CHANNEL_NOT_HAS_CATEGORY', 'value': '4001', 'intro': u'该频道下没有可用栏目'},
        {'code': 'CHANNEL_INVALID', 'value': '4002', 'intro': u'无效的频道'},
        {'code': 'CHANNEL_CATEGORY_INVALID', 'value': '4003', 'intro': u'无效的栏目'},
        {'code': 'CHANNEL_PUSH_INVALID', 'value': '4004', 'intro': u'无效的推送栏目'},
        {'code': 'CHANNEL_CATEGORY_TYPE_INVALID', 'value': '4005', 'intro': u'无效的栏目类型'},
        {'code': 'CHANNEL_OCCUPIED_KEY', 'value': '4006', 'intro': u'频道或栏目关键字重复'},
        {'code': 'CHANNEL_CATEGORY_TYPE_CANNOT_CHANGE', 'value': '4007', 'intro': u'该栏目下有文章，不可更换栏目类型'},
        {'code': 'CHANNEL_CATEGORY_CANNOT_DELETE', 'value': '4008', 'intro': u'该栏目下有文章，不可删除栏目'},
        {'code': 'CHANNEL_CATEGORY_DIRECT_CONFLICT', 'value': '4009', 'intro': u'该类型的栏目不可设为单文直达'},
        {'code': 'CHANNEL_WRITE_FILE_FAIL', 'value': '4010', 'intro': u'PDF文件写入失败'},
        {'code': 'CHANNEL_WRITE_FILE_ERRFILE', 'value': '4012', 'intro': u'错误的文件类型'},

        {'code': 'ARTICLE_PAGER_OUT_OF_INDEX', 'value': '5000', 'intro': u'查询无数据'},
        {'code': 'ARTICLE_ID_INVALID', 'value': '5001', 'intro': u'无效的文章编号'},
        {'code': 'ARTICLE_DIFFERENT_CATE_TYPE', 'value': '5002', 'intro': u'不可将文章同时发到不同类型的栏目中'},
        {'code': 'ARTICLE_CANNOT_CHANGE_CATE_TYPE', 'value': '5003', 'intro': u'不可将文章修改到不同类型的栏目中'},
        {'code': 'ARTICLE_PASS_CANNOT_DELETE', 'value': '5004', 'intro': u'教师不能删除已经审批通过文章'},
        {'code': 'ARTICLE_TEACHER_ONLY_CAN_DELETE_SELF', 'value': '5005', 'intro': u'教师不能删除他人发布的文章'},
        {'code': 'ARTICLE_PASS_CANNOT_MODI', 'value': '5006', 'intro': u'教师不能修改已经审批通过文章'},

        {'code': 'COMMON_SYS_PARA_NOT_EXIST', 'value': '6000', 'intro': u'系统参数不存在'},

        {'code': 'QUICKFUNC_ID_INVALID', 'value': '7000', 'intro': u'无效的快速功能链接ID编号'},

        {'code': 'PICTURE_ID_INVALID', 'value': '8000', 'intro': u'无效的轮播图ID编号'},
        {'code': 'PICTURE_NOPIC', 'value': '8001', 'intro': u'请上传图片'},
        {'code': 'PICTURE_SAVE_FAIL', 'value': '8002', 'intro': u'保存轮播图失败'},
    ]

    dict_resp = {"c": 0, "m": u'请求完成', "d": data}
    return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")


def get_msg(type):
    return {'c': type[0], 'm': type[1]}

