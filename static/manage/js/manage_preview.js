var article_id = $("#article_id").text();

$(function() {
    new Vue({
        el: '#main',
        data: {
            detail: {
                publish_time: ''
            }
        },
        ready: function () {
            var self = this;

            // 文章详情
            if(article_id === ''){
                // 即时预览
                $.ajax({
                    url: "/api/manage/article/preview",
                    type: "POST",
                    data: {
                        "is_preview": '1'
                    },
                    success: function (data) {
                        if (data.c == 0) {
                            self.detail = data.d;
                        }
                    }
                });
            } else {
                $.ajax({
                    url: "/api/manage/article/get",
                    type: "POST",
                    data: {
                        "id": article_id
                    },
                    success: function (data) {
                        if (data.c == 0) {
                            self.detail = data.d;
                        }
                    }
                });
            }
        },
        watch: {
			detail: function () {
                // 自动播放第一个视频
                //$($(".detail video")[0]).attr("autoplay", "autoplay");

                // 图片大小调整
                function resizepic(thispic) {
                    var width = $(thispic).width();
                    if (width > 800) {
                        $(thispic).css("width", "100%");
                    }
                }
                $(".detail img").each(function(){
                    resizepic(this);
                    $(this).load(function(){
                        resizepic(this);
                    });
                });

                $('#video').bind('contextmenu',function() {
                    //取消鼠标右键功能，禁止视频下载
                    return false;
                });
			}
  		}
    })
});
