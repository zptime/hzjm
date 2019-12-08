# -*- coding=utf-8 -*-

import os
from platform import platform


DEBUG = False if 'centos' in platform() else True

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '0f$@gun=@7es+9t%m%u7xl$g&kqar$ptt-xpc99lkdn6j_fmjn'

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'app_account.User'

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'app_common',
    'app_account',
    'app_site',
    'app_swagger',
    'chunked_upload',
    'upload_resumable',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

SUIT_CONFIG = {
    'ADMIN_NAME': u'武汉汉字解密数据库管理',
    'HEADER_DATE_FORMAT': 'Y年 F j日 l',
    'HEADER_TIME_FORMAT': 'H:i',
    'LIST_PER_PAGE': 50,
    'MENU': (
        {'app': 'app_account', 'label': u'账户', 'icon': 'icon-user',},
        {'app': 'app_common', 'label': u'通用', 'icon': 'icon-user',},
        {'app': 'app_site', 'label': u'站点', 'icon': 'icon-user',},
    )
}

ROOT_URLCONF = 'hzjm.urls'

WSGI_APPLICATION = 'hzjm.wsgi.application'

if DEBUG:
    HOST = '127.0.0.1'#'10.89.154.245'
    DB_NAME = 'hbedu_hzjm'
    DB_USER = 'liukai'#'admin'
    DB_PWD = 'liukai'
else:
    # 生产环境数据库账号密码
    HOST = '127.0.0.1'
    DB_NAME = 'hbedu_hzjm'
    DB_USER = 'admin'
    DB_PWD = 'fhcloud86Fh12#$'
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PWD,
        'HOST': HOST,
        'PORT': '3306',
    }
}

SITE_ID = 1
LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
TIME_FORMAT = 'H:i'

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html': True,
        # },
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'hzjm.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'hzjm.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
        'django.db.backends_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR + '/log/', 'db.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['default', 'console'],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.db.backends': {
            'handlers': ['django.db.backends_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

# 此处的Ueditor配置会覆盖ueditor.config.js的配置项
UEDITOR_SETTINGS = {
    'config': {

    },
    'upload': {
        "imageMaxSize": 2048000,
        "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".PNG", ".JPG", ".JPEG", ".GIF", ".BMP"],
        "videoMaxSize": 51200000000,
        "videoAllowFiles": [".flv", ".swf", ".mkv", ".avi", ".mpeg", ".mpg", ".mov", ".wmv", ".mp4", ".mp3", ".wav",
                            ".FLV", ".SWF", ".MKV", ".AVI", ".MPEG", ".MPG", ".MOV", ".WMV", ".MP4", ".MP3", ".WAV"],
        "fileMaxSize": 8192000,
        "fileAllowFiles": [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp",
            ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg", ".mov", ".wmv", ".mp4",
            ".mp3", ".wav",
            ".rar", ".zip", "7z",
            ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml",
            ".PNG", ".JPG", ".JPEG", ".GIF", ".BMP",
            ".FLV", ".SWF", ".MKV", ".AVI", ".RM", ".RMVB", ".MPEG", ".MPG", ".MOV", ".WMV", ".MP4",
            ".MP3", ".WAV",
            ".RAR", ".ZIP", ".7Z",
            ".DOC", ".DOCX", ".XLS", ".XLSX", ".PPT", ".PPTX", ".PDF", ".TXT", ".MD", ".XML"
        ]
    }
}

LOGIN_URL='/login'

CHUNKED_UPLOAD_PATH = os.path.join(BASE_DIR, "media/temp/upload_chunk")

# upload_resumable
TMP_DIR = os.path.join(BASE_DIR, 'tmp_file')
DATA_STORAGE_USE_S3 = False   # 是否采用S3对象存储
DATA_STORAGE_USE_S3_HOST_URL = False  # 若该参数为真，文件URL使用S3 HOST做为域名
DATA_STORAGE_USE_ABSOLUTE_URL = False  # 默认是否采用绝对地址
FILE_STORAGE_DIR_NAME = "media"
