$(function(){

	/**渲染nav栏*/
	function render_nav(){
		if ($('#view_val').val()){
			view_val = $('#view_val').val();
			$('#'+view_val).prepend('<el class="li-active-tag"></el>');
			$('#'+view_val).children('a').addClass('active');
		}
	}

	 //切换左侧视图
	$('.main_left li').on('click',function(){
		var view_val = $(this).val();
		//$(this).prepend('<el class="li-active-tag"></el>');
		//$(this).children('a').addClass('active');
		//url_go( '/index?nav='+$('#nav_val').val()+'&view='+ b.id);
	});
});
