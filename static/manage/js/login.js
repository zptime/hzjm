$(function(){
    var is_browser_valid = false;
    if(true == jQuery.browser.mozilla){
        is_browser_valid = true
    }
    if(true == jQuery.browser.chrome){
        is_browser_valid = true
    }
    if(true == jQuery.browser.msie){
       if(parseInt(jQuery.browser.version)>8){
           is_browser_valid = true
       }
    }
    if(false == is_browser_valid){
        var user_browser = jQuery.browser.name + ' ' + jQuery.browser.version;
        layer.open({
            type: 1,
            area: ['540px', '250px'], //宽高
            title:'错误',
            content: "<div class='content_layer'><div>您的浏览器太老了！<br>" +
            "请使用 <b><font color='red'>Chrome、Firefox、搜狗浏览器(极速模式)、360安全浏览器(极速模式)</font></b> 等浏览器！</div></div>",
            closeBtn: 0,
            btn:['下载Chrome浏览器']
            ,yes: function(index, layero){
                var elemIF = document.createElement("iframe");
                elemIF.src = '/media/tool/chrome.exe';
                elemIF.style.display = "none";
                document.body.appendChild(elemIF);
            }
        });
    }

    $('#username').keypress(function(event){
        if(event.keyCode == 13){
            $('#login').click();
        }
    });

    $('#password').keypress(function(event){
        if(event.keyCode == 13){
            $('#login').click();
        }
    });

   $("#login").click(function(){
       // 登录
       var username = $("#username").val();
       var password = $("#password").val();
       if(!username.match(/^[a-zA-Z0-9_]{4,20}$/)){
           $("#username").focus();
           layer.msg("帐号不合法：4-20字母、数字、下划线");
       }else if(!password.match(/^.{6,16}$/)){
           $("#password").focus();
           layer.msg("密码不合法：6-16字符");
       } else {
           $.ajax({
               url: "/api/manage/user/login",
               type: "POST",
               data: {
                   'username': username,
                   "password": password
               },
               success: function (data) {
                   if (data.c == 0) {
                       if(data.d.role == '0'){
                           window.location.href = "/page/manage/article/program";
                       } else {
                           window.location.href = "/page/manage/article/mine";
                       }
                   } else {
                       layer.msg(data.m);
                   }
               },
               error:function (data) {
                   layer.msg("系统错误，请稍候重试！")
               }
           });
       }
   })
});
