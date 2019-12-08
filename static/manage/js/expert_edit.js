$(function() {
    new Vue({
        el: '#main',
        data: {
            article_id:'',
            detail: {
                "expert_id": '',
                "expert_name":'',
                "expert_sortorder":'',
                "expert_article_num":'',
                "expert_image":'',
                "expert_intro":''
            }
        },
        ready: function () {
            var self = this;
            self.article_id=getQueryString('id');

            if(self.article_id !== ''){
                // 专家详情
                $.ajax({
                    url: "/api/manage/expert/get",
                    type: "POST",
                    data: {
                        "expert_id": self.article_id
                    },
                    success: function (data) {
                        if (data.c == 0) {
                            self.detail = data.d;
                        }
                    }
                });
            }
        },
        methods: {
            cancelDraft: function() {
                window.history.go(-1);
            },
            previewDraft: function() {
                var self = this;

                if(self.checkRequiredFields()){
                    layer.msg("请输入必填项！");
                } else {
                    var formData = new FormData($("#dataForm")[0]);
                    formData.append("is_preview",'1');
                    if(self.article_id === '') {
                        // 新增预览
                        self.sendPreviewRequest("/api/manage/expert/add", formData);
                    } else {
                        // 修改预览
                        formData.append("expert_id",self.article_id);
                        self.sendPreviewRequest("/api/manage/expert/edit", formData);
                    }
                }
            },
            sendPreviewRequest: function(url, formData) {
                $.ajax({
                    url: url,
                    type: "POST",
                    data: formData,
                    async: false,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        if (data.c == 0) {
                            window.open("/page/manage/expert/preview?id="+data.d.expert_id+"&is_preview=1");
                        } else {
                            layer.msg(data.m)
                        }
                    }
                });
            },
            saveDraft: function() {
                var self = this;

                if(self.checkRequiredFields()){
                    layer.msg("请输入必填项！");
                } else {
                    // 按钮置灰再发请求
                    $(".content_btn button").addClass("disabled").attr("disabled", "true");

                    var formData = new FormData($("#dataForm")[0]);
                    if(self.article_id === '') {
                        // 新增保存
                        self.sendSaveRequest("/api/manage/expert/add", formData);
                    } else {
                        // 修改保存
                        formData.append("expert_id",self.article_id);
                        self.sendSaveRequest("/api/manage/expert/edit", formData);
                    }
                }
            },
            sendSaveRequest: function(url, formData) {
                $.ajax({
                    url: url,
                    type: "POST",
                    data: formData,
                    async: false,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (data) {
                        if (data.c == 0) {
                            window.location.href = "/page/manage/article/expert";
                        } else {
                            layer.msg(data.m)
                        }
                    }
                });
            },
            checkRequiredFields: function() {
                var self = this;
                var requireFlag = false;
                $.each($("#dataForm .require"), function(i,n) {
                    if(($(n).parent().next().is('input'))&&($(n).parent().next().val()==='')){
                        // 输入框
                        requireFlag = true;
                    } else if(self.detail.expert_image===''){
                        // 照片
                        requireFlag = true;
                    }
                });

                return requireFlag;
            },
            selectPic:function () {
                $('input[name="expert_image"]').click();
            },
            pushImage:function () {
                var self=this;
                var tempSrc = window.URL.createObjectURL($(".image")[0].files[0]);
                self.detail.expert_image = tempSrc;
            }
        },
        watch:{
            detail:function () {
                var text = document.getElementById("textarea");
                autoTextarea(text);// 调用
            }
        }
    })
});
