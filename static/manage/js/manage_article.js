$(function(){
    new Vue({
        el: '#main',
        data: {
			idList: [],
			admit_state: '',
			is_push: '',
			title_key: ''
        },
        ready: function () {
			var self = this;
			$('.main_left li#program').prepend('<el class="li-active-tag"></el>');
			$('.main_left li#program').children('a').addClass('active');
			self.getTableData();

			$("#titleKey").keypress(function(event){
				if(event.keyCode == 13){
					self.tableFilter();
				}
    		});
        },
		methods: {
			getTableData: function() {
				var self = this;
				$(".grid").html('<table id="grid"></table><div id="pager"></div>');
				//表格数据加载
				$("#grid").jqGrid({
					url : '/api/manage/article/list',
					datatype : "json",
					mtype:"POST",//ajax提交方式
					postData: {
						'title_key': self.title_key
					},
					jsonReader : {
						 root: "d.rows",   // json中代表实际模型数据的入口
						 page: "d.page",   // json中代表当前页码的数据
						 total: "d.total", // json中代表页码总数的数据
						 records: "d.records" // json中代表数据行总数的数据
					 },
					autowidth: true,
					height: 'auto',
					colNames:['id','标题','讲解专家','发布时间','操作'],
					colModel:[
						{name:'id',index:'id', hidden:true},
						{name:'title',index:'title',align:'center'},
						{name:'expert_name',index:'expert_name', width:60, align:"center"},
						{name:'publish_time',index:'publish_time', width:120, align:"center"},
						{name:'oper',index:'oper', formatter: fmt_oper,width:60, align:"center"}
					],
					rowNum : 20,//设置表格中显示的记录数，参数会被自动传到后台。
					pager : '#pager',
					altRows: true,//是否允许单双行样式不同
					altclass: 'zebra',
					sortable: false,
					multiselect:true,
					multiselectWidth:18,//多选框宽度
					multiboxonly: false, //是否只有点击多选框时
					gridview: true, //加速显示
					viewrecords: false,//显示总记录数
					pagerpos: "center", //指定分页栏的位置
					beforeSelectRow:function(rowid, e){//当点击的单元格的名字为cb时，才触发选择行事件
						if(e.type == 'click'){
							i = $.jgrid.getCellIndex($(e.target).closest('td')[0])
								cm = jQuery("#grid").jqGrid('getGridParam', 'colModel');
							return (cm[i].name == 'cb');
						}
						return false;
					},
					loadComplete: function() {//如果数据不存在，提示信息
						var rowNum = $("#grid").jqGrid('getGridParam','records');
						if (rowNum ==0||rowNum==null){
							if($("#norecords").html() == null){
								$("#grid").parent().append("</pre> <div id='norecords'>没有查询记录！</div> <pre>");
							}
							$("#norecords").show();
						}else{//如果存在记录，则隐藏提示信息。
							$("#norecords").hide();
						}
					},
					gridComplete: function() {//当表格所有数据都加载完成，处理统计行数据
						$('#first_pager').remove();
						$('#last_pager').remove();
						$('#prev_pager').attr('title','上一页');
						$('#next_pager').attr('title','下一页');
						$('.ui-separator').remove();
						var rowNum = $(this).jqGrid('getGridParam','records');//获取当前jqGrid的总记录数；
						$('#total_record').text(rowNum);

						var childspan = $("#input_pager").children('.ui-pg-input').next();
						var childinput = $("#input_pager").children('.ui-pg-input');
						$("#input_pager").empty().append(childinput);

						var el = document.createElement("td");
						$(el).attr('id','grid_next_pager_countinfo').html('共'+childspan.html()+'页');
						if ( $('#grid_next_pager_countinfo').length == 0){
							$('#next_pager').after(el);
						}

						var el2=document.createElement('select');
						$(el2).attr('class','jqgh_grid_type_select').html('<option value="1">当页</option><option value="2">全部</option>');
						$('#grid_type').empty().append(el2);

						// 点击表格行推送查看详情
						$('.fa-eye').click(function(){
							layer.tips($(this).text(), '#'+$(this).attr('id'));
						})
					},
					onSelectRow:function(rowid,status){
						self.idList=$("#grid").jqGrid('getGridParam','selarrrow');
					},
					onSelectAll:function(rowid, status) {
						self.idList=$("#grid").jqGrid('getGridParam','selarrrow');
					}
				});

				//操作栏事件
				function fmt_oper(cellvalue, options, rowObject){
					return '<div class="grid-btn"><a href="/page/manage/preview?articleid='+rowObject.id+'" target="_blank">预览</a></div><div class="grid-btn"><a href="/page/manage/draft?articleid='+rowObject.id+'">修改</a></div>';
				}
			},
			tableFilter: function() {
				var self = this;
				self.getTableData();
			},
			articleAdd: function() {
				window.location.href = "/page/manage/draft";
			},
			articleDelete: function() {
				var self = this;
				layer.confirm('确定删除所选文章吗？', {
					title: '确认',
				    btn: ['取消','确定'] //按钮
				}, function(index){
					layer.close(index);
				}, function(){
				    self.sendRequest("/api/manage/article/delete");
				});
			},
			sendRequest: function(url) {
				var self = this;
				$.ajax({
					url: url,
					type: "POST",
					data: {
						'id_list':self.idList.toString()
					},
					success: function (data) {
						if (data.c == 0) {
							layer.msg("操作成功");
							self.idList = [];
							$("#grid").trigger("reloadGrid");
						} else {
							layer.msg(data.m)
						}
					},
					error:function (data) {
						layer.msg("系统错误，请稍候重试！")
					}
				});
			}
		}
    })
});
