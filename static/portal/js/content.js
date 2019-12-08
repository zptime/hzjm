var article_id = $("#article_id").text();

$(function() {
    new Vue({
        el: '#main',
        data: {
            detail: {
                'publish_time': ''
            }
        },
        ready: function () {
            var self = this;
            $.ajax({
                url: "/api/hzjm/article/get",
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
        },
        watch: {
			detail: function () {
                //$($(".detail video")[0]).attr("autoplay", "autoplay");

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
                })
			}
  		}
    })
});

