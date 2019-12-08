# -*- coding: utf-8 -*-

import logging

from app_common.models import *


logger = logging.getLogger(__name__)


def load_sys_para():
    sys_qs = CommonParameter.objects.filter(is_delete=False, is_allow_config=True)
    sys_list = list()
    for each_sys in sys_qs:
        sys_list.append({
            'id': int(each_sys.id),
            'key': each_sys.key,
            'value': each_sys.value1,
            'name': each_sys.name,
        })
    return sys_list
