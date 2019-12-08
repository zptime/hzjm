# coding:utf-8
import re
import os, time, random
import datetime
import types
import math
import socket
from functools import wraps
from json import JSONEncoder

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
import json
from decimal import getcontext, Decimal
import base64
import hmac
import hashlib
import sha

import app_site
from err_code import REQUEST_PARAM_ERROR

helper = __import__('utils')


FORMAT_DATE = "%Y-%m-%d"
FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S"
FORMAT_YEAR = "%Y"

FORMAT_DATE_CODE = 1
FORMAT_DATETIME_CODE = 2
FORMAT_YEAR_CODE = 3


def safe_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def is_duplicate_field(value, model_name, field_name):
    model_clazz = getattr(app_site.models, model_name)
    query_para = {
        'is_delete': False,
        field_name: value
    }
    return model_clazz.objects.filter(**query_para).exists()


def datetime2str(datetime_para, format=FORMAT_DATETIME):
    """
        时间转字符串
    """
    if not datetime_para:
        return ''
    return datetime_para.strftime(format)


def bool2str(bool_para):
    """
        布尔值转字符串
    """
    return '1' if bool_para else '0'


def str2bool(str_para):
    """
        字符串转布尔值
    """
    return False if str_para == '0' else True


def require_roles(allow=None):
    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            if request.user.role not in allow:
                # return HttpResponse(JSONEncoder().encode({'result': 'fail', 'reason': u'没有权限访问此接口'}) \
                #                     , content_type="application/json", status=403)
                raise PermissionDenied
            return func(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def str2datetime(datetime_str):
    """
    功能说明：   str日期转换为时间,YYYY-mm-dd hh:mm:ss
    """
    try:
        day = datetime.datetime.strptime(datetime_str, FORMAT_DATETIME)
    except:
        day = datetime.datetime.now()
    return day


def check_identity_no(id):
    id = id.upper()
    # 身份证验证
    c = 0
    for (d, p) in zip(map(int, id[:~0]), range(17, 0, -1)):
        c += d * (2 ** p) % 11
    return id[~0] == '10X98765432'[c % 11]


# 验证账号格式
def is_mobile(mobile):
    if mobile:
        if len(mobile) == 11 and re.match("^(1[34587]\d{9})$", mobile) != None:
            return True
        else:
            return False
    else:
        return False


# 判断是否为整数
def IsNumber(varObj):
    if varObj:
        if re.match("^([0-9]*)$", varObj) != None:
            return True
        else:
            return False
    else:
        return False


def is_qq(qq):
    if qq:
        if re.match("^([1-9][0-9]{4,})$", qq) != None:
            return True
        else:
            return False
    else:
        return False


# 判断是否为字符串 string
def IsString(varObj):
    return type(varObj) is types.StringType


# 判断是否为浮点数 1.324
def IsFloat(varObj):
    return type(varObj) is types.FloatType


# 判断是否为字典 {'a1':'1','a2':'2'}
def IsDict(varObj):
    return type(varObj) is types.DictType


# 判断是否为tuple [1,2,3]
def IsTuple(varObj):
    return type(varObj) is types.TupleType


# 判断是否为List [1,3,4]
def IsList(varObj):
    return type(varObj) is types.ListType


# 判断是否为布尔值 True
def IsBoolean(varObj):
    return type(varObj) is types.BooleanType


# 判断是否为货币型 1.32
def IsCurrency(varObj):
    # 数字是否为整数或浮点数
    if IsFloat(varObj) and IsNumber(varObj):
        # 数字不能为负数
        if varObj > 0:
            return True
    return False


# 判断某个变量是否为空 x
def IsEmpty(varObj):
    if len(varObj) == 0:
        return True
    return False


# 判断变量是否为None None
def IsNone(varObj):
    return type(varObj) is types.NoneType


# 判断是否为日期格式,并且是否符合日历规则 2010-01-31
def IsDate(varObj):
    if len(varObj) == 10:
        rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
        match = re.match(rule, varObj)
        if match:
            return True
        return False
    return False


# 判断是否为邮件地址
def IsEmail(varObj):
    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match(rule, varObj)
    if match:
        return True
    return False


# 判断是否为中文字符串
def IsChineseCharString(varObj):
    for x in varObj:
        if (x >= u"\u4e00" and x <= u"\u9fa5") or (x >= u'\u0041' and x <= u'\u005a') or (
                        x >= u'\u0061' and x <= u'\u007a'):
            continue
        else:
            return False
    return True


# 判断是否为中文字符
def IsChineseChar(varObj):
    if varObj[0] > chr(127):
        return True
    return False


# 匹配IP地址
def IsIpAddr(varObj):
    rule = '\d+\.\d+\.\d+\.\d+'
    match = re.match(rule, varObj)

    if match:
        return True
    return False

# 清除空格
def clear_str_space(s):
    s = s.replace(' ', '')
    s = s.replace(u'　', '')
    return s


def generate_code(length):
    num = '0123456789'
    return ''.join(random.sample(num, length))


def generate_captcha(length):
    return [generate_code(length)]


def random_int_len(start, end, length):
    nums = range(start, end)
    data = random.sample(nums, length)
    return data


def makename(name):
    # 文件扩展名
    ext = os.path.splitext(name)[1]

    # 定义文件名，年月日时分秒随机数
    fn = time.strftime('%Y%m%d%H%M%S')
    fn += '_%d' % random.randint(1, 10000)
    # 重写合成文件名
    name = fn + ext
    return name


def getno():
    t = int(time.time())
    r = random.randint(10, 99)
    s = datetime.datetime.now().microsecond / 1000
    no = str(t) + str(s) + str(r)
    return no


def distance(lat1, lng1, lat2, lng2):
    if lat1 and lng1 and lat2 and lng2:
        R = 6378137
        radLat1 = math.radians(lat1)
        radLng1 = math.radians(lng1)
        radLat2 = math.radians(lat2)
        radLng2 = math.radians(lng2)

        s = math.acos(
            math.cos(radLat1) * math.cos(radLat2) * math.cos(radLng1 - radLng2) + math.sin(radLat1) * math.sin(
                radLat2)) * R
        s = round(s * 10000) / 10000
        return round(s)
    else:
        return 0


def the_months(dt):
    # 本月初
    month = dt.month
    year = dt.year
    day = 1
    return dt.replace(year=year, month=month, day=day)


def last_months(dt):
    # 上月初
    month = dt.month - 1
    if month == 0:
        month = 12
    year = dt.year - month / 12
    day = 1
    return dt.replace(year=year, month=month, day=day)


def next_months(dt):
    # 下月初
    month = dt.month
    year = dt.year + month / 12
    month = month % 12 + 1
    day = 1
    return dt.replace(year=year, month=month, day=day)


def last_year(dt):
    # 明年初
    year = dt.year - 1
    month = 1
    day = 1
    return dt.replace(year=year, month=month, day=day)


def next_year(dt):
    # 明年初
    year = dt.year + 1
    month = 1
    day = 1
    return dt.replace(year=year, month=month, day=day)


def the_year(dt):
    # 年初
    year = dt.year
    month = 1
    day = 1
    return dt.replace(year=year, month=month, day=day)


def begin_time(dt):
    return dt.replace(minute=0, second=0)


def divmodA(a, b):
    tmp1, tmp2 = divmod(a, b)
    if tmp2 > 0:
        return tmp1 + 1
    else:
        return tmp1





def getCurrentDate():
    """
            获取当前日期：2013-09-10这样的日期字符串
    """
    return time.strftime(FORMAT_DATE, time.localtime(time.time()))


def getCurrentDateTime():
    """
            获取当前时间：2013-09-10 11:22:11这样的时间年月日时分秒字符串
    """
    return time.strftime(FORMAT_DATETIME, time.localtime(time.time()))


def getCurrentHour():
    """
            获取当前时间的小时数，比如如果当前是下午16时，则返回16
    """
    currentDateTime = getCurrentDateTime()
    return currentDateTime[-8:-6]


def getDateElements(sdate):
    """
            输入日期字符串，返回一个结构体组，包含了日期各个分量
            输入：2013-09-10或者2013-09-10 22:11:22
            返回：time.struct_time(tm_year=2013, tm_mon=4, tm_mday=1, tm_hour=21, tm_min=22, tm_sec=33, tm_wday=0, tm_yday=91, tm_isdst=-1)
    """
    dformat = ""
    if judgeDateFormat(sdate) == 0:
        return None
    elif judgeDateFormat(sdate) == FORMAT_DATE_CODE:
        dformat = FORMAT_DATE
    elif judgeDateFormat(sdate) == FORMAT_DATETIME_CODE:
        dformat = FORMAT_DATETIME
    sdate = time.strptime(sdate, dformat)
    return sdate


def getDateToNumber(date1):
    """
            将日期字符串中的减号冒号去掉:
            输入：2013-04-05，返回20130405
            输入：2013-04-05 22:11:23，返回20130405221123
    """
    return date1.replace("-", "").replace(":", "").replace("", "")


def judgeDateFormat(datestr):
    """
            判断日期的格式，如果是"%Y-%m-%d"格式则返回1，如果是"%Y-%m-%d %H:%M:%S"则返回2，否则返回0
            参数 datestr:日期字符串
    """
    try:
        datetime.datetime.strptime(datestr, FORMAT_DATE)
        return FORMAT_DATE_CODE
    except:
        pass

    try:
        datetime.datetime.strptime(datestr, FORMAT_DATETIME)
        return FORMAT_DATETIME_CODE
    except:
        pass

    try:
        datetime.datetime.strptime(datestr, FORMAT_YEAR)
        return FORMAT_YEAR_CODE
    except:
        pass

    return 0


def minusTwoDate(date1, date2):
    """
            将两个日期相减，获取相减后的datetime.timedelta对象
            对结果可以直接访问其属性days、seconds、microseconds
    """
    if judgeDateFormat(date1) == 0 or judgeDateFormat(date2) == 0:
        return None
    d1Elements = getDateElements(date1)
    d2Elements = getDateElements(date2)
    if not d1Elements or not d2Elements:
        return None
    d1 = datetime.datetime(d1Elements.tm_year, d1Elements.tm_mon, d1Elements.tm_mday, d1Elements.tm_hour,
                           d1Elements.tm_min, d1Elements.tm_sec)
    d2 = datetime.datetime(d2Elements.tm_year, d2Elements.tm_mon, d2Elements.tm_mday, d2Elements.tm_hour,
                           d2Elements.tm_min, d2Elements.tm_sec)
    return d1 - d2


def dateAddInDays(date1, addcount):
    """
            日期加上或者减去一个数字，返回一个新的日期
            参数date1：要计算的日期
            参数addcount：要增加或者减去的数字，可以为1、2、3、-1、-2、-3，负数表示相减
    """
    try:
        addtime = datetime.timedelta(days=int(addcount))
        d1Elements = getDateElements(date1)
        d1 = datetime.datetime(d1Elements.tm_year, d1Elements.tm_mon, d1Elements.tm_mday)
        datenew = d1 + addtime
        return datenew.strftime(FORMAT_DATE)
    except Exception as e:
        print e
        return None


def is_leap_year(pyear):
    """
            判断输入的年份是否是闰年
    """
    try:
        datetime.datetime(pyear, 2, 29)
        return True
    except ValueError:
        return False


def dateDiffInDays(date1, date2):
    """
            获取两个日期相差的天数，如果date1大于date2，返回正数，否则返回负数
    """
    minusObj = minusTwoDate(date1, date2)
    try:
        return minusObj.days
    except:
        return None


def dateDiffInSeconds(date1, date2):
    """
            获取两个日期相差的秒数
    """
    minusObj = minusTwoDate(date1, date2)
    try:
        return minusObj.days * 24 * 3600 + minusObj.seconds
    except:
        return None


def getWeekOfDate(pdate):
    """
            获取日期对应的周，输入一个日期，返回一个周数字，范围是0~6、其中0代表周日
    """
    pdateElements = getDateElements(pdate)

    weekday = int(pdateElements.tm_wday) + 1
    if weekday == 7:
        weekday = 0
    return weekday


def get_host_ip():
    """
            获取当前IP地址
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    # ip = myaddr + ":8080"
    return myaddr


def get_full_sever_address():
    """
        获取服务器完url path地址
    """
    return "http://"+get_host_ip()


def get_expires(m):
    expires = datetime.datetime.now() + datetime.timedelta(minutes=m)
    timestamp = str(int(time.mktime(expires.timetuple()))) + '000'
    return timestamp


def mask_words(words, content):
    """
    功能说明：   替换敏感词
    """
    try:
        if words:
            lst = words.split(',')
            for w in lst:
                content = content.replace(w, '**')
    except Exception as e:
        pass
    return content


def remove_html_tag(html):
    """
    功能说明：   去除html标签
    """
    reg = re.compile('<[^>]*>')
    return reg.sub('', html)


def is_password_legal(password):
    """
    功能说明：   判断密码是否合法
    """
    if not password or len(password) < 6 or len(password) > 20:
        return False
    return True


def day_to_str(date):
    """
    功能说明：   日期转换为str,YYYY-mm-dd
    """
    day = ''
    try:
        day = date.strftime(FORMAT_DATE)
    except:
        pass
    return day


def str_to_day(datestr):
    """
    功能说明：   str日期转换为时间,YYYY-mm-dd
    """
    day = datetime.datetime.now()
    try:
        day = datetime.datetime.strptime(datestr, FORMAT_DATE)
    except:
        pass
    return day


def daytime_to_str(date):
    """
    功能说明：   日期转换为str,YYYY-mm-dd hh:mm:ss
    """
    day = ''
    try:
        day = date.strftime(FORMAT_DATETIME)
    except:
        pass
    return day


def str_to_daytime(datestr):
    """
    功能说明：   str日期转换为时间,YYYY-mm-dd hh:mm:ss
    """
    day = datetime.datetime.now()
    try:
        day = datetime.datetime.strptime(datestr, FORMAT_DATETIME)
    except:
        pass
    return day


def year_to_str(date):
    """
    功能说明：   年份转换为str,YYYY
    """
    day = ''
    try:
        day = date.strftime(FORMAT_YEAR)
    except:
        pass
    return day


def str_to_year(datestr):
    """
    功能说明：   str年转换为时间年,YYYY
    """
    day = datetime.datetime.now()
    try:
        day = datetime.datetime.strptime(datestr, FORMAT_YEAR)
    except:
        pass
    return day


def response(result):
    """
    功能说明：   返回json
    """
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")

def respformat(message):
    """
    将错误信息按照cmd格式转换
    """
    return {"c": REQUEST_PARAM_ERROR[0], "m": message}


def int_to_weekday(num):
    """
    功能说明：   数字转换为周几
    """
    day = num % 7
    if day == 0:
        return u'周日'
    if day == 1:
        return u'周一'
    if day == 2:
        return u'周二'
    if day == 3:
        return u'周三'
    if day == 4:
        return u'周四'
    if day == 5:
        return u'周五'
    if day == 6:
        return u'周六'


def get_file_size_str(size):
    """
    功能说明：   计算文件大小，long转为str
    """
    if size < 1024:
        return str(size) + u'B'
    elif 1024 <= size < 1024*1024:
        value = Decimal(size/1024.0).quantize(Decimal('0.00'))
        return str(value) + u'KB'
    elif 1024*1024 <= size < 1024*1024*1024:
        value = Decimal(size/1024.0/1024.0).quantize(Decimal('0.00'))
        return str(value) + u'MB'
    else:
        value = Decimal(size/1024.0/1024.0/1024.0).quantize(Decimal('0.00'))
        return str(value) + u'GB'


def get_half_year_ago_date():
    """
    功能说明：   获取半年前的时间
    """
    now_time = datetime.datetime.now()
    return now_time + datetime.timedelta(days=-178)


# def read_excel(excel_path, type):
#     """
#     创建用户和群组之间的关系,不是成员的时候，新建成员，是成员的时候修改角色信息
#     :param parent:家长类型用户
#     :param student:学生类型用户
#     :return: relation
#     """
#     try:
#         url = u'''D:/python_project/vschool/media/temp/files/teacher_模板.xls'''
#         excel = xlrd.open_workbook(url)
#         table = excel.sheets()[0]
#         total_row = table.nrows  # 总行数
#         total_col = table.ncols  # 总列数
#         first_row = table.row_values(0)  # 第一行的数据
#         data_list = []
#         for row in range(1, total_row):
#             row_value = table.row_values(row)
#             if row_value:
#                 app = []
#                 for i in range(total_col):
#                     if IsFloat(row_value[i]) or IsNumber(row_value[i]):
#                         app.append(str(int(row_value[i])))
#                     else:
#                         app.append(row_value[i])
#                 data_list.append(app)
#         return data_list
#     except Exception as e:
#         print('read_excel Exception:%s' % str(e))
#         return {}


def generate_images():
    """
    生成表情部分的代码
    :return:
    """
    try:
        files = os.listdir('D:\python_project\\vschool\static\img\\faces_56')# 路径可以自己
        test = "["
        for name in files:
            newname = name.replace('.png', '')  # .py也是可以修改
            tt = newname.decode('gbk').encode('utf-8')
            print tt
            test = test + "'" + tt+"',"
        test += "]"
        print test
    except Exception as e:
        print('Exception:%s' % str(e))


if __name__ == "__main__":
    # timestrap = 1470197107809
    # time = datetime.datetime.fromtimestamp(timestrap/1000)
    # print str(time)
    size = get_file_size_str(1245254)
    print size

    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    timestamp = '2016-08-16 18:42:49'
    print timestamp

    h = hmac.new(key='OtxrzxIsfpFjA7SwPzILwy8Bw21TLhquhboDYROV', msg=timestamp, digestmod=hashlib.sha256)
    cal_signature = base64.encodestring(h.digest()).strip()
    print cal_signature


    # datas = read_excel(1, 3)
    # for item in datas:
    #     print item
    # generate_images()
#     time = get_half_year_date()
#     print(time.strftime(FORMAT_DATETIME))
#     print get_file_size_str(345345)
#     print judgeDateFormat("2013-04-01")
#     print judgeDateFormat("2013-04-01 21:22:33")
#     print judgeDateFormat("2013-04-31 21:22:33")
#     print judgeDateFormat("2013-xx")
#     print "--"
#     print datetime.datetime.strptime("2013-04-01", "%Y-%m-%d")
#     print 'elements'
#     print getDateElements("2013-04-01 21:22:33")
#     print 'minus'
#     print minusTwoDate("2013-03-05", "2012-03-07").days
#     print dateDiffInSeconds("2013-03-07 12:22:00", "2013-03-07 10:22:00")
#     print type(getCurrentDate())
#     print getCurrentDateTime()
#     print dateDiffInSeconds(getCurrentDateTime(), "2013-06-17 14:00:00")
#     print getCurrentHour()
#     print dateAddInDays("2013-04-05", -5)
#     print getDateToNumber("2013-04-05")
#     print getDateToNumber("2013-04-05 22:11:33")
#
#     print getWeekOfDate("2013-10-01")


def getpages(cnt, page, size):
    """
     分页，这种方式比Paginator更高效一些
    :param:总行数， 当前页码  ，每页行数
    :return: 总页数，本次开始行数，本次结束行数
    """
    import math
    # 分页，这种方式比Paginator更高效一些
    if not page or not size:
        return 1, 0, cnt

    page = int(page)
    size = int(size)
    num_pages = math.ceil(float(cnt) / size)  # 总页数
    # if page > num_pages:
    #     raise BusinessException(MOMENT_NORECORD)
    cur_start = (page - 1) * size
    cur_end = page * size
    return num_pages, cur_start, cur_end


if __name__ == '__main__':
    pass