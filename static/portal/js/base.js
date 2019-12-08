$(function(){
    // 检测浏览器内核版本，文档模式IE9以下弹出提示
	if(jQuery.browser.msie){
        if(document.documentMode<9){
            layer.open({
				type: 1,
				title: false,
				area: ['1200px', '80%'], //宽高
				content: '<div class="content_layer">'+
					'<p>您使用的浏览器内核版本太老，请下载并使用新的谷歌Chrome浏览器： <a class="browser_download" href="/media/tool/chrome.exe">下载谷歌浏览器</a></p>' +
					'<p>如果您在使用双核浏览器，例如360浏览器、搜狗浏览器、QQ浏览器、猎豹浏览器等，也可以切换模式来继续访问，操作如下：</p>' +
					'<p>1. QQ浏览器</p>'+
					'<img src="/static/portal/img/guide_qq.png">'+
					'<p>点击右上角的闪电，选择“极速模式”。</p>'+
					'<p>2. 搜狗浏览器</p>'+
					'<img src="/static/portal/img/guide_sougo.png">'+
					'<p>点击红圈中的标识，直至切换为“闪电”状态。</p>'+
					'<p>其他双核浏览器操作类似。</p>'+
				'</div>',
				closeBtn: 0
			});
        }
    }

    // 打开后台管理快捷键Ctrl+Alt+O
	function Hotkey(event, ctrlKey, shiftKey, altKey, keycode) {
		if (event.ctrlKey == ctrlKey && event.shiftKey == shiftKey && event.altKey == altKey && event.keyCode == keycode){
			window.open("/page/manage/home");
		}
	}

	function fnKeyup(event) {
		Hotkey(event, true, false, true, 79);
	}
	if (document.addEventListener)
		document.addEventListener("keyup",fnKeyup,true);
	else
		document.attachEvent("onkeyup",fnKeyup);

	$("#searchInput").val('');

    $("#searchInput").keydown(function(event){
        if(event.which == "13"){
             $("#searchBtn").click();
        }
    });

    $("#searchBtn").click(function(){
        var searchStr = $.trim($("#searchInput").val());
        if(searchStr !== ''){
            window.location.href = "/page/hzjm/find?searchkey="+escape(searchStr);
        }
    })
});
