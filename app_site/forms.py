# -*- coding=utf-8 -*-

from DjangoUeditor.forms import UEditorField
from django import forms


class CommonUeditorForm(forms.Form):
    content = UEditorField('', initial='', width=800, height=800
         , settings={'toolbars': [
            ['source', 'fullscreen', 'undo', 'redo', 'cleardoc', '|', 'fontfamily', 'fontsize', 'bold', 'italic', 'underline', 'strikethrough','justifyleft', 'justifyright', 'justifycenter', 'forecolor', 'backcolor'],
            ['inserttable', 'inserttitle', 'insertrow', 'insertcol', 'mergeright', 'mergedown', 'deleterow', 'deletecol', 'splittorows', 'splittocols', 'splittocells', 'deletecaption', 'mergecells', 'deletetable', 'edittable', 'edittd', '|', 'simpleupload', 'insertimage', 'insertvideo', 'imageleft', 'imageright', 'imagecenter', '|', 'attachment']
        ]})


class PhotoUeditorForm(forms.Form):
    content = UEditorField('', initial='', width=800, height=800
         , settings={'toolbars': [
            ['fullscreen', 'undo', 'redo', 'cleardoc', '|', 'simpleupload', 'insertimage', 'imageleft', 'imageright', 'imagecenter']
        ]})