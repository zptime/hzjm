# -*- coding: utf-8 -*-

import os
import subprocess

from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from chunked_upload.models import ChunkedUpload
from chunked_upload.exceptions import ChunkedUploadError

from django.shortcuts import render_to_response

from json import *


class ChunkedUpload(ChunkedUpload):
    pass


# Override the default ChunkedUpload to make the `user` field nullable
ChunkedUpload._meta.get_field('user').null = True


class ChunkedUploadView(ChunkedUploadView):

    model = ChunkedUpload
    field_name = 'the_file'

    def check_permissions(self, request):
        if not hasattr(request, 'user'):
            raise ChunkedUploadError(
                status=403,
                result='fail',
                reason=u'必须先登录才可以上传作品'
            )
        if hasattr(request, 'user') and not request.user.is_authenticated():
            raise ChunkedUploadError(
                status=403,
                result='fail',
                reason=u'无权限上传作品'
            )

        upload_file = request.FILES[self.field_name]
        if not upload_file.name.upper().endswith('PDF'):
            raise ChunkedUploadError(
                status=400,
                result='fail',
                reason=u'仅支持%s格式的作品上传' % 'PDF'
            )

class ChunkedUploadCompleteView(ChunkedUploadCompleteView):

    model = ChunkedUpload

    def check_permissions(self, request):
        if not hasattr(request, 'user'):
            raise ChunkedUploadError(
                status=403,
                result='fail',
                reason=u'必须先登录才可以上传作品'
            )
        if hasattr(request, 'user') and not request.user.is_authenticated():
            raise ChunkedUploadError(
                status=403,
                result='fail',
                reason=u'无权限上传作品'
            )

    def on_completion(self, uploaded_file, request):
        # close uploaded file first
        uploaded_file.file.close()

    def get_response_data(self, chunked_upload, request):
        return {'result': 'success'}

