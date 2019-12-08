$(function(){
    $(".setting").mouseover(function(){
		$(".user_btn").show();
	}).mouseleave(function(){
		$(".user_btn").slideUp();
	});

	// 修改密码
	$("#changepw").click(function(){
		layer.open({
			  type: 1,
			  area: ['540px', '300px'], //宽高
			  title:'修改密码',
			  content: $('#changepwForm'),
			  btn:['取消','确定']
			  ,yes: function(index, layero){
				 //按钮【取消】的回调
				 layer.close(index);
				 return false;
			  },btn2: function(index, layero){
					//按钮【确定】的回调
					var requireFlag = false;
					$.each($("#changepwForm .require"), function(i,n) {
						if($(n).parent().next().val()===''){
							requireFlag = true;
						}
					});
					if(requireFlag){
						layer.msg("请输入必填项！");
						return false;
					} else if(!$("#newpw").val().match(/^.{6,16}$/)){
						layer.msg("密码不合法：6-16字符");
						return false;
					} else if($("#newpw").val() !== $("#newpw_repeate").val()) {
						layer.msg("两次密码不一致！");
						return false;
					} else {
						$.ajax({
							url: "/api/manage/user/changepw",
							type: "POST",
							data: new FormData($("#changepwForm")[0]),
							async: false,
							cache: false,
							contentType: false,
							processData: false,
							success: function (data) {
								if (data.c == 0) {
									layer.msg("操作成功");
									window.location.href = '/login';
								} else {
									layer.msg(data.m)
								}
							}
						});
					}
			  }
		});
	});

    // 退出
    $("#logout").click(function(){
       layer.confirm('确定退出吗？', {
           title: '确认',
           btn: ['取消','确定'] //按钮
       }, function(index){
           layer.close(index);
       }, function(){
           $.ajax({
               url: "/api/manage/user/logout",
               type: "GET",
               success: function (data) {
                   if (data.c == 0) {
                       window.location.href = "/login";
                   } else {
                       layer.msg(data.m);
                   }
               },
               error:function (data) {
                   layer.msg("系统错误，请稍候重试！")
               }
           });
       });
    })
});
