/**
 * Created by Administrator on 2018/1/22.
 */
PER_PAGE_RECORD = 24; //每页显数示记录数

$(function() {
    new Vue({
        el: '#main',
        data: {
            current_page: '',
        	expert_id:'',//存储页面获取的id
            expert: {
                 'total': 1
            },
            article:{
        	    'total': 1
            }
        },
        ready: function () {
            var self = this;
            $('.title a.expert-title').css('color','#ff595f');
            $('.title a.expert-title').after('<hr>');
            self.expert_id = getQueryString('expert_id');
            self.queryExpertList();
            self.queryArticleList(1);

            // 翻页跳转
            $("#page").keydown(function(event){
                if(event.which == "13"){
                    self.queryExpertList(Number($("#page").val()));
                    $("#page").val("").blur();
                }
            });
        },
        methods: {
            queryExpertList: function() {
                var self = this;
                $.ajax({
                    url: "/api/manage/expert/get",
                    type: "POST",
                    data: {
                        "expert_id": self.expert_id
                    },
                    success: function (data) {
                        if (data.c == 0) {
                            self.expert = data.d;
                        }
                    }
                });
            },
            queryArticleList: function(page) {
                var self = this;
                 var page = page <= self.article.total ? page : self.article.total;
                $.ajax({
                    url: "/api/manage/article/list",
                    type: "POST",
                    data: {
                        "expert_id": self.expert_id,
                        "page": page,
                        "rows": PER_PAGE_RECORD
                    },
                    success: function (data) {
                        if (data.c == 0) {
                            self.article = data.d;
                            self.current_page = page;
                        }
                    }
                });
            },
            imageShow:function () {
                var ele=eventCompatible();
                $(ele).parents('.block').find('.play_video').css('display','block');
                $(ele).parents('.block').find('.text').addClass('border-shadow');
            },
            imageHidden:function () {
                var ele=eventCompatible();
                $(ele).parents('.block').find('.play_video').css('display','none');
                $(ele).parents('.block').find('.text').removeClass('border-shadow');
            }
        },
        watch:{
            expert:function () {
                var text = document.getElementById("textarea");
                autoTextarea(text);// 调用
            }
        }
    })
});