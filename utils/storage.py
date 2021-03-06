# -*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import SuspiciousOperation
from django.conf import settings
from django.core.files.base import ContentFile
# from PIL import Image
# import const
import StringIO


class Storage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(Storage, self).__init__(location, base_url)

    @property
    def maxsize(self):
        return 10 * 1024 * 1024

    @property
    def filetypes(self):
        return []

    def delete(self, name):
        super(Storage, self).delete(name)


class FileStorage(Storage):
    @property
    def maxsize(self):
        return 20 * 1024 * 1024

    @property
    def filetypes(self):
        return ['fasta', 'hla', 'final', 'apk', 'ipa']

    # def _save(self, name, content):
    #     ext = name.split(".")[-1]
    #     #类型判断
    #     # if self.filetypes != '*':
    #     #     if ext.lower() not in self.filetypes:
    #     #         raise SuspiciousOperation('file type error!')
    #
    #     #大小判断
    #     if content.size > self.maxsize:
    #         raise SuspiciousOperation('file size error!')
    #
    #     return super(FileStorage, self)._save(name, content)


class ImageStorage(Storage):
    @property
    def maxsize(self):
        return 5 * 1024 * 1024

    @property
    def filetypes(self):
        return ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'flv', 'swf']

    def _save(self, name, content):
        import os, time, random
        ext = name.split(".")[-1]
        # 类型判断
        if self.filetypes != '*':
            if ext.lower() not in self.filetypes:
                raise SuspiciousOperation(100)

        # 大小判断
        if content.size > self.maxsize:
            raise SuspiciousOperation(222)

        # 文件改名
        d = os.path.dirname(name)
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        # 重写合成文件名
        name = os.path.join(d, fn + '.' + ext)

        return super(ImageStorage, self)._save(name, content)


# class ThumbStorage(ImageStorage):
#
#     def _save(self, name, content):
#         image = Image.open(content)
#         if image.mode not in ('L', 'RGB'):
#             image = image.convert('RGB')
#
#         width, height = image.size
#         size = 320
#         if width > size:
#             delta = width / size
#             height = int(height / delta)
#             image.thumbnail((size, height), Image.ANTIALIAS)
#
#         output = StringIO.StringIO()
#         image.save(output, 'JPEG')
#         co = ContentFile(output.getvalue())
#         output.close()
#
#         return super(ThumbStorage, self)._save(name, co)
