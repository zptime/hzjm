#!/usr/bin/python
# -*- coding=utf-8 -*-
import re
import types


class InvalidParaException(Exception):
    def __init__(self, description):
        super(InvalidParaException, self).__init__(description)


def get_parameter(para, para_intro='', allow_null=False, default=None, valid_check=None, **valid_check_para):
    """
        统一请求入参检查方法
        注意：默认不允许请求入参为空 allow_null=False
             允许为空的情况下，默认值默认是None default=None
    """
    if None is para or para == '':
        if not allow_null:
            raise InvalidParaException('参数"%s"值不合法' % para_intro)
        else:
            return default

    if valid_check:
        # 校验函数只有一个
        if type(valid_check) == types.FunctionType:
            if not valid_check(para, **valid_check_para):
                raise InvalidParaException('参数"%s"值不合法' % para_intro)
        # 校验函数有多个（元组或者列表）
        elif type(valid_check) == types.TupleType or type(valid_check) == types.ListType:
            for each_check in valid_check:
                if callable(each_check):
                    if not each_check(para, **valid_check_para):
                        raise InvalidParaException('参数"%s"值不合法' % para_intro)
    return para


def INTEGER(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是整型
    """
    try:
        int(para)
    except:
        return False
    else:
        return True


def ACCOUNT(para, **valid_check_para):
    """
        判断账号是否合法 ，允许4-20字节，允许字母数字下划线
    """
    print '123'
    return True if re.match('^[a-zA-Z0-9_]{4,20}$', para) else False


def PASSWORD(para, **valid_check_para):
    """
        判断密码是否合法，允许6-16字节
    """
    return True if re.match('^.{6,16}$', para) else False


def INTEGER_NONNEGATIVE(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是非负整数
    """
    try:
        int_value = int(para)
    except:
        return False
    else:
        return int_value >= 0


def INTEGER_POSITIVE(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是正整数
    """
    try:
        int_value = int(para)
    except:
        return False
    else:
        return int_value > 0


def INTEGER_IN_RANGE(para, **valid_check_para):
    """
        检查传入参数（字符串格式）是否是在某一范围的整型
    """
    try:
        int_value = int(para)
    except:
        return False
    else:
        return True if int_value \
                in range(valid_check_para.get('min'), valid_check_para.get('max')+1) else False


def CHOICES(para, **valid_check_para):
    """
        检查传入参数，是否是给定枚举内的一种
    """
    return True if para in valid_check_para.get('choices') else False


def LENGTH(para, **valid_check_para):
    return len(para) <= valid_check_para.get('length')


if __name__ == "__main__":
    # 测试用例
    try:
        # print get_parameter('10', '每月每人在每班默认发放奖章个数', valid_check=INTEGER)
        # print get_parameter('100', '每月每人在每班默认发放奖章个数', valid_check=INTEGER_IN_RANGE, min=1, max=100)
        # print get_parameter('-20', '每月每人在每班默认发放奖章个数', valid_check=INTEGER_NONNEGATIVE)
        # print get_parameter('1', '家长能否发这个奖章', valid_check=(CHOICES,INTEGER_IN_RANGE), choices=('1','1000', 'ai'), min=1, max=100)
        # print get_parameter(None, '每月每人在每班默认发放奖章个数', allow_null=True, default='5', valid_check=INTEGER)

        # print type(LENGTH) == types.FunctionType

        print True if re.match('^[a-zA-Z][a-zA-Z0-9_]{3,15}$', 'teacher02') else False
    except InvalidParaException as ipe:
        print ipe.message
