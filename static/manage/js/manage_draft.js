var article_id = $("#article_id").text();

$(function() {
    new Vue({
        el: '#main',
        data: {
            detail: {
                id: '',
                image: '',
                video_upload_id:'',
                video_upload_name:''
            },
            expert:[],
            img_in_content: []
        },
        ready: function () {
            var self = this;

            if(article_id !== ''){
                // 文章详情
                $.ajax({
                    url: "/api/manage/article/get",
                    type: "POST",
                    async:false,
                    data: {
                        "id": article_id
                    },
                    success: function (data) {
                        if (data.c == 0) {
                            self.detail = data.d;
                            var str=self.detail.video_path;
                            var index = str.lastIndexOf("\/");
                            self.detail["video_upload_name"]=str.substring(index + 1, str .length);
                        }
                    }
                });
            }

            // 专家列表
            $.ajax({
                url: "/api/manage/expert/list",
                type: "POST",
                success: function (data) {
                    if (data.c == 0) {
                        self.expert = data.d.expert_list;

                        $.each(self.expert,function (index,value) {
                            if(self.detail.expert_id==value.expert_id){
                                $("select").append("<option value=\"" + value.expert_id + "\" selected>" + value.expert_name + "</option>");
                            }else{
                                $("select").append("<option value=\"" + value.expert_id + "\">" + value.expert_name + "</option>");
                            }
                        });

                        $('#expert_select').searchableSelect({
                            afterSelectItem: function(){
                                self.detail.expert_id=this.holder.data("value");
                            }
                        });
                    }
                }
            });

            laydate({
                elem: '#publishTime',
                format: 'YYYY-MM-DD hh:mm:ss',
                start: laydate.now(0, "YYYY-MM-DD hh:mm:ss"),
                isclear: false,
                istime: true,
                istoday: true,
                choose: function(datas){
                }
            });
        },
        methods: {
            selectPic: function() {
                var self = this;

                // 查找编辑框中的图片
                var imgs = [];
                $.each(document.getElementById('ueditor_0').contentWindow.document.getElementsByTagName('img'), function(){
                    if($(this).attr("class")===undefined){
                         imgs.push($(this).attr("src"));
                    }
                });
                self.img_in_content = imgs;

                // 选中当前封面
                $(".fa-check-circle").removeClass("fa-check-circle").addClass("fa-circle-thin");
                $('#picForm img[src="'+self.detail.image+'"]').parent().next().removeClass("fa-circle-thin").addClass("fa-check-circle");

                layer.open({
				    type: 1,
				    area: ['540px', '300px'], //宽高
				    title:'从本地选择一张图片或从正文中选择一张图片',
				    content: $('#picForm'),
				    btn:['取消','确定']
				    ,yes: function(index, layero){
					    //按钮【取消】的回调
					    layer.close(index);
					    return false;
                    },btn2: function(index, layero){
					    //按钮【确定】的回调
                        if($(".fa-check-circle").length === 0){
                            layer.msg('请先选择一张图片！');
                            return false;
                        } else {
                             self.detail.image = $(".fa-check-circle").prev().children().attr("src");
                        }
                    }
				});
            },
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
                    if(article_id === '') {
                        // 新增预览
                        self.sendPreviewRequest("/api/manage/article/add", formData);
                    } else {
                        // 修改预览
                        formData.append("id",article_id);
                        self.sendPreviewRequest("/api/manage/article/edit", formData);
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
                            window.open("/page/manage/preview?is_preview=1");
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
                    formData.append("image_url", self.detail.image);
                    if(article_id === '') {
                        // 新增保存
                        self.sendSaveRequest("/api/manage/article/add", formData);
                    } else {
                        // 修改保存
                        formData.append("id",article_id);
                        self.sendSaveRequest("/api/manage/article/edit", formData);
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
                            window.location.href = "/page/manage/article/program";
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
                    if($(n).parent().next().attr("class")==="edit-area"){
                        // 富文本框
                        var editor = UE.getEditor('id_content');
                        editor.sync();
                        if(editor.hasContents()==false){
                            requireFlag = true;
                        }
                    } else if(($(n).parent().next().is('input'))&&($(n).parent().next().val()==='')){
                        // 输入框
                        requireFlag = true;
                    } else if(self.detail.image===''){
                        // 封面
                        requireFlag = true;
                    }
                });

                return requireFlag;
            },
            uploadVideo:function () {
                var self=this;
                layer.open({
                    type: 2,
                    title: "上传视频",
                    content: '/page/upload',
                    area:["700px","400px"],
                    cancel: function () {
                        layer.close();
                    }
                });
            }
        }
    })
});
