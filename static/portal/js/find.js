PER_PAGE_RECORD = 24; //每页显数示记录数
var searchkey = $("#searchkey").text();

$(function() {
    new Vue({
        el: '#main',
        data: {
            searchkey: unescape(searchkey),
            current_page: '',
            article: {
                 'total': 1
            }
        },
        ready: function () {
            var self = this;
            self.queryArticleList(1);

            // 翻页跳转
            $("#page").keydown(function(event){
                if(event.which == "13"){
                    self.queryArticleList(Number($("#page").val()));
                    $("#page").val("").blur();
                }
            });
        },
        methods: {
            queryArticleList: function(page) {
                var self = this;
                // 若入参大于总页数，则默认跳到末页
                var page = page <= self.article.total ? page : self.article.total;
                $.ajax({
                    //url:"/static/mock/list.json",
                    url: "/api/hzjm/article/search",
                    type: "POST",
                    data: {
                        "key": unescape(searchkey),
                        "page": page,
                        "rows": PER_PAGE_RECORD
                    },
                    success: function (data) {
                        //var data=JSON.parse(data);
                        if (data.c == 0) {
                            // 标题关键字标红
                            $.each(data.d.rows, function(index, row){
                                row.title = row.title.replace(eval("/"+self.searchkey+"/gi"), '<span class="red">'+self.searchkey+'</span>')
                            });

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
        }
    })
});
