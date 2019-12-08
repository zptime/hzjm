#!/usr/bin/python
# -*- coding: utf-8 -*-

from operLog.models import COperLog

#增加操作日志
def add_operLog(user,new_obj):
    lstDesc = []
    meta = new_obj._meta

    for field in meta.fields:
        val = eval("new_obj.%s" % field.name)
        if not val:
            continue

        for tmp1, tmp2 in field.choices:
            if tmp1 == val:
                val = tmp2
                break

        lstDesc.append("%s(%s):%s," % (field.verbose_name, field.name, val))

    desc = "\r\n".join(lstDesc)
    if hasattr(new_obj, "id"):
        object = "id=%s" % (new_obj.id)
    else:
        object = ""

    oOperLog = COperLog(user=user, opType="1", table=meta.db_table, opObj=object, desc=desc)
    oOperLog.save()

def modify_operLog(user, old_obj, new_obj, changed_data):
    #修改
    lstDesc = []
    meta = new_obj._meta
    for field in meta.fields:
        if field.name not in changed_data:
            continue

        old_val = old_obj[field.name]
        new_val = eval("new_obj.%s" % field.name)

        lstDesc.append("%s(%s):%s --> %s " % (field.verbose_name, field.name, old_val, new_val))

    desc = "\r\n".join(lstDesc)
    if hasattr(new_obj, "id"):
        object = "id=%s" % (new_obj.id)
    else:
        object = ""

    oOperLog = COperLog(user=user, opType="3", table=meta.db_table, opObj=object, desc=desc)
    oOperLog.save()

# def modifyTypeLog2(user, org_obj, change_data):
#     #修改
#     lstDesc = []
#     new_meta = org_obj._meta
#     for key, val in change_data.items():
#         lstDesc.append("[%s --> %s] " % (key, val))
#     # for (i, field) in enumerate(new_meta.fields):
#     #     new_val = eval("new_obj.%s" % field.name)
#     #     org_val = eval("obj.%s" % field.name)
#     #     if new_val != org_val:
#     #         for tmp1, tmp2 in field.choices:
#     #             if tmp1 == new_val:
#     #                 new_val = tmp2
#     #             elif tmp1 == org_val:
#     #                 org_val = tmp2
#     #         lstDesc.append("[%s:%s --> %s] " % (field.verbose_name, org_val, new_val))
#
#     desc = "\r\n".join(lstDesc)
#     object = "%s id=%s" % (new_meta.verbose_name, org_obj.id)
#     oOperLog = COperLog(user=user, oper="3", object=object, desc=desc)
#     oOperLog.save()

#删除
def del_operLog(user, new_obj):
    meta = new_obj._meta

    lstDesc = []

    for field in meta.fields:
        val = eval("new_obj.%s" % field.name)
        # if not val:
        #     continue
        new_val = eval("new_obj.%s" % field.name)
        lstDesc.append("%s(%s):%s," % (field.verbose_name, field.name, val))

    desc = "\r\n".join(lstDesc)
    if hasattr(new_obj, "id"):
        object = "id=%s" % (new_obj.id)
    else:
        object = ""

    oOperLog = COperLog(user=user, opType="2", table=meta.db_table, opObj=object, desc=desc)
    oOperLog.save()