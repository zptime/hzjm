# -*- coding: utf-8 -*-

from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app_site.views_chunkupload import *
from hzjm import settings


# 数据库管理
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'', include('upload_resumable.urls')),
]

# swagger
urlpatterns += patterns('app_swagger.views',
     url(r'^api/$', 'api_index'),
     url(r'^api/docs/$', 'api_docs'),
)

# 页面跳转
urlpatterns += patterns('templates.pages',
    url(r'^$', 'portal_index'),  # 进入门户首页
    url(r'^page/hzjm/article/list$', 'portal_article_list'),  # 进入某栏目的文章列表页面  ?columnkey=xxx
    url(r'^page/hzjm/find$', 'portal_search'),   # 进入搜索页面  ?searchkey=xxx
    url(r'^page/hzjm/content$', 'portal_content'),   # 进入正文页面  ?articleid=xxx
	url(r'^page/hzjm/expert$', 'portal_expert'),  # 进入专家介绍页面
	url(r'^page/hzjm/expert_content$', 'portal_expert_content'),  # 进入专家介绍页面

    url(r'^login$', 'manage_login'),  # 进入登录页面
    url(r'^page/upload$', 'page_upload'),
    url(r'^page/manage/pendlist$', 'manage_pendlist'),  # 进入待审核文章列表页面
    url(r'^page/manage/user$', 'manage_user'),   # 进入用户管理页面
    url(r'^page/manage/article/program$', 'manage_article'),   # 进入节目管理页面
    url(r'^page/manage/article/expert', 'manage_expert'),   # 进入专家管理页面
    url(r'^page/manage/expert/edit', 'expert_edit'),  # 进入专家新增、编辑页面
    url(r'^page/manage/expert/preview', 'expert_preview'),  # 进入专家预览页面
    url(r'^page/manage/article/mine$', 'manage_article_teacher'),   # 进入教师文章管理页面
    url(r'^page/manage/article/push$', 'manage_article_push'),  # 进入文章管理页面（推送）
    url(r'^page/manage/draft$', 'manage_draft'),    # 进入新增文章页面  ?article_id=xxx
    url(r'^page/manage/preview$', 'manage_preview'),    # 进入文章预览查看页面  ?article_id=xxx
    url(r'^page/manage/sys$', 'manage_sys'),   # 进入其它配置页面
    url(r'^page/manage/mine$', 'manage_mine'),   # (教师) 进入我的文章页面
    url(r'^page/manage/home$', 'manage_home'),   # 登录进入我的文章页面
)

# 异步api请求 - 通用部分
urlpatterns += patterns('app_common.views',
    url(r'^api/common/tmppic/add$', 'common_tmp_pic_add'),
    url(r'^api/common/sys/list$', 'common_sys_list'),
    url(r'^api/common/sys/edit$', 'common_sys_edit'),
)

# 异步api请求 - 门户部分
urlpatterns += patterns('app_site.views_portal',
    url(r'^api/hzjm/article/search$', 'portal_article_search'),
    url(r'^api/hzjm/article/list$', 'portal_article_list'),
    url(r'^api/hzjm/article/get$', 'portal_article_get'),
)

# 异步api请求 - 分块上传部分
urlpatterns += patterns('app_site.views_chunkupload',
    url(r'^chunked_upload/?$', ChunkedUploadView.as_view(), name='api_chunked_upload'),
    url(r'^chunked_upload_complete/?$', ChunkedUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
)


# 异步api请求 - 管理部分

# 异步api请求 - 账号部分
urlpatterns += patterns('app_account.views',
    url(r'^api/manage/user/login$', 'manage_user_login'),
    url(r'^api/manage/user/logout$', 'manage_user_logout'),
    url(r'^api/manage/user/changepw$', 'manage_user_changepw'),

)

# 异步api请求 - 帮助
urlpatterns += patterns('utils.err_code',
    url(r'^api/help/errcode/list$', 'helper_errcode_list'),
)
urlpatterns += patterns('app_site.views_manage',
    # 专家
    url(r'^api/hzjm/expert/list$', 'manage_expert_list'),
    url(r'^api/manage/expert/list$', 'manage_expert_list'),
    url(r'^api/manage/expert/get$', 'manage_expert_get'),
    url(r'^api/manage/expert/add$', 'manage_expert_add'),
    url(r'^api/manage/expert/edit$', 'manage_expert_edit'),
    url(r'^api/manage/expert/delete$', 'manage_expert_delete'),

    # 文章
    url(r'^api/manage/article/list$', 'manage_article_list'),
    url(r'^api/manage/article/get$', 'manage_article_get'),
    url(r'^api/manage/article/preview$', 'manage_article_preview'),
    url(r'^api/manage/article/add$', 'manage_article_add'),
    url(r'^api/manage/article/edit$', 'manage_article_edit'),
    url(r'^api/manage/article/delete$', 'manage_article_delete'),
)
urlpatterns += patterns('utils.const',
    url(r'^api/help/const/list$', 'helper_const_list'),
)


# 如果使用调试模式，需要使用django的静态文件处理器来访问media文件
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve',
                                {'document_root': settings.MEDIA_ROOT,}),
                            )