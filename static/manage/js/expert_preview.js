$(function() {
    new Vue({
        el: '#main',
        data: {
            article_id:'',
            expert:{}
        },
        ready: function () {
            var self = this;
            self.article_id=getQueryString('id');

            // 专家详情
            $.ajax({
                url: "/api/manage/expert/get",
                type: "POST",
                data: {
                    "expert_id": self.article_id
                },
                success: function (data) {
                    if (data.c == 0) {
                        self.expert = data.d;
                    }
                }
            });
        },
        watch:{
            expert:function () {
                var text = document.getElementById("textarea");
                autoTextarea(text);// 调用
            }
        }
    })
});
