/**
 * Created by Administrator on 2018/1/22.
 */
PER_PAGE_RECORD = 15; //每页显数示记录数

$(function() {
    new Vue({
        el: '#main',
        data: {
            current_page: '',
            expert: {
                 'total': 1
            }
        },
        ready: function () {
            var self = this;
            self.queryExpertList(1);

            $('.title a.expert-title').css('color','#ff595f');
            $('.title a.expert-title').after('<hr>');

            // 翻页跳转
            $("#page").keydown(function(event){
                if(event.which == "13"){
                    self.queryExpertList(Number($("#page").val()));
                    $("#page").val("").blur();
                }
            });
        },
        methods: {
            queryExpertList: function(page) {
                var self = this;
                // 若入参大于总页数，则默认跳到末页
                var page = page <= self.expert.total ? page : self.expert.total;
                $.ajax({
                    url: "/api/manage/expert/list",
                    type: "POST",
                    data: {
                        "page": page,
                        "rows": PER_PAGE_RECORD
                    },
                    success: function (data) {
                        if (data.c == 0) {
                            self.expert = data.d;
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
                $(".expert_detail").each(function(i){
                    var divH = $(this).height();
                    var $p = $("p", $(this)).eq(0);
                    while ($p.outerHeight() > divH) {
                        $p.text($p.text().replace(/(\s)*([a-zA-Z0-9]+|\W)(\.\.\.)?$/, "..."));
                    }
                });
            }
        }
    })
});
