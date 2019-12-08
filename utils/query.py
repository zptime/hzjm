# -*- coding: utf-8 -*-
from django.db import connection


def select(sql, columns):
    if sql is None or sql == "":
        return
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        fetchall = cursor.fetchall()
        object_lis = []
        if fetchall:
            for obj in fetchall:
                row = {}
                for index, c in enumerate(columns):
                    row[c] = obj[index]
                object_lis.append(row)
        return object_lis

    except Exception, e:
        print e
        print sql
        print columns
        return []


def pagination_page(sql, columns, count_sql, page_no, page_num):
    """
    功能说明:     分页处理（获取当前页数据,和页面属性）
    ======================================================
    sql         —— 所有数据 sql 语句
    columns     —— 页面数据属性名,与 sql 的查询结果一一对应
    count_sql   —— 数据总数 sql 语句/也可以传数字
    page_no     —— 页码
    page_num    —— 每页数据量
    =======================================================
    返回数据:
    =======================================================
    {
        "list":[],        —— 页面数据
        "page_attr":[1,65,""]   ——页面属性[页码,总页数,url]
    }
    =======================================================
    """
    if sql is None or sql == "":
        return None
    try:
        cursor = connection.cursor()
        if isinstance(count_sql, int):
            count = count_sql
        else:
            cursor.execute(count_sql)
            count = cursor.fetchall()[0][0]     # 数据总数
        bc = count % page_num
        if bc == 0:
            pages = count/page_num
        else:
            pages = (count/page_num)+1 if bc < page_num else 0    # 总页数
        # 页面数据
        sql += """ limit %s,%s""" % ((int(page_no)-1)*page_num, page_num)
        cursor.execute(sql)
        fetchall = cursor.fetchall()
        object_lis = []        # 页面数据
        if fetchall:
            for obj in fetchall:
                row = {}
                for index, c in enumerate(columns):
                    row[c] = obj[index]
                object_lis.append(row)
        return {'list': object_lis, 'cur_page': page_no, 'page_size': pages, 'row_size': count}

    except Exception, e:
        print e
        print sql
        print columns
        return {}


def pagination_start(sql, columns, count_sql, start, length, paging=True):
    """
    功能说明:     分页处理（获取当前页数据,和页面属性）
    ======================================================
    sql         —— 所有数据 sql 语句
    columns     —— 页面数据属性名,与 sql 的查询结果一一对应
    count_sql   —— 数据总数 sql 语句/也可以传数字
    start     —— 起始记录
    length    —— 数据长度
    paging --是否分页查询
    =======================================================
    返回数据:
    =======================================================
    {
        "list":[],        —— 页面数据
    }
    =======================================================
    """
    if sql is None or sql == "":
        return None
    try:
        cursor = connection.cursor()

        if isinstance(count_sql, int):
            count = count_sql
        else:
            cursor.execute(count_sql)
            count = cursor.fetchall()[0][0]     # 数据总数

        if paging:
            bc = count % length
            if bc == 0:
                pages = count/length
            else:
                pages = (count/length)+1 if bc < length else 0    # 总页数

            # 页面数据
            sql += """ limit %s,%s""" % (start, length)
        else:
            pages = 1

        cursor.execute(sql)
        fetchall = cursor.fetchall()
        object_lis = []        # 页面数据
        if fetchall:
            for obj in fetchall:
                row = {}
                for index, c in enumerate(columns):
                    row[c] = obj[index]
                object_lis.append(row)

        return {'list': object_lis, 'start': start, 'pages': pages, 'row_size': count}

    except Exception, e:
        print e
        print sql
        print columns
        return {}
