# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.http import require_POST

from app_common import services
from app_common.models import *
from utils import utils_common
from utils.err_code import *
from utils.para_check import *
from utils.utils_common import require_roles, respformat

logger = logging.getLogger(__name__)


@require_GET
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def common_sys_list(request):
    """
        列出所有可以修改的系统配置参数
    """
    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1], "d": services.load_sys_para()}
    return utils_common.response(dict_resp)


@require_POST
@login_required
@require_roles(allow=(DB_USER_ROLE_ADMIN,))
def common_sys_edit(request):
    """
        修改某一个系统配置参数
    """
    try:
        id = get_parameter(request.POST.get('id'), para_intro='系统参数配置ID编号', valid_check=INTEGER_NONNEGATIVE)
        value = get_parameter(request.POST.get('value'), para_intro='参数新的配置值', allow_null=True, default='')
    except InvalidParaException as ipe:
        return utils_common.response(respformat(ipe.message))

    sys_para = CommonParameter.objects.filter(is_delete=False, id=id).first()
    if not sys_para:
        return utils_common.response(get_msg(COMMON_SYS_PARA_NOT_EXIST))

    sys_para.value1 = value
    sys_para.save()

    dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1]}
    return utils_common.response(dict_resp)


@login_required
@require_POST
def common_tmp_pic_add(request):
    """
        提交一张临时图片
        /api/common/tmppic/add
    """
    try:
        image = request.FILES.get('file', None)
        if not image:
            return utils_common.response(get_msg(REQUEST_PARAM_ERROR))

        image_temp = CommonImageTemp()
        image_temp.image = image
        # size = image_temp.image.size
        # image_temp.size = utils.get_file_size_str(size)
        image_temp.size = str(image_temp.image.size)
        image_temp.name = image_temp.image.name
        image_temp.save()

        dict_resp = {"c": REQUEST_SUCCESS[0], "m": REQUEST_SUCCESS[1],
                     "d": {'url': image_temp.image.url, 'id': image_temp.pk}}
        return HttpResponse(json.dumps(dict_resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception(e)
        return HttpResponse(json.dumps({"c": -1, "m": str(e)}, ensure_ascii=False), content_type="application/json")
