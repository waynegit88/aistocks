<template>

	<div class="mainpage" >
		<span :key="key"></span>  <!-- for update page purpose -->
		<el-container style="height: 100%; width: 100%; position: absolute;" direction="vertical" id = "rootForm">
			<el-header class="shadow" style="height: 55px; opacity: 0.6;">
				<div>
					<el-button class="font-Logo" type="text" style="float:left; font-weight:bold; font-size:20px;">
						AIStocks
					</el-button>
				</div>
				<div>
					<el-button plain round class="fRight" id="logout" @click="logout">Logout</el-button>
				</div>
			</el-header>
			<el-main>
				<el-container style="height: 100%; width: 100%; ">
					<el-aside width="264px">
						<el-row class="buttonback" style="display: flex; justify-content: stretch; padding: 0px; width: 100%">
							<el-button-group size="mini" style="display: flex; justify-content: stretch; padding: 0px;">
						      <el-button :type = "btntype_sha" class="groupbutton" value="沪A" @click="selectstocktype">
								  沪A</el-button>
						      <el-button :type = "btntype_sza" class="groupbutton" value="深A" @click="selectstocktype">
								  深A</el-button>
							  <el-button :type = "btntype_zxb" class="groupbutton" value="中小" @click="selectstocktype">
								  中小</el-button>
						      <el-button :type = "btntype_kcb" class="groupbutton" value="科创" @click="selectstocktype">
								  科创</el-button>
						      <el-button :type = "btntype_cyb" class="groupbutton" value="创业" @click="selectstocktype">
								  创业</el-button>
							  <el-button :type = "btntype_zxg" class="groupbutton" value="自选" @click="selectstocktype">
								  自选</el-button>
							</el-button-group>
						</el-row>
						<el-row>
						    <el-table 
								v-loading="stockListLoading"
    							element-loading-text="正在获取股票列表..."
    							element-loading-spinner="el-icon-loading"
    							element-loading-background="rgba(0, 0, 0, 0.8)"
								:data="tabledata" style="width: 100%; font-size:14px;" :show-header=false 
								:row-style="rowstyle" :cell-style="{padding:'0px'}" @row-click="stockRowClick">
						      <el-table-column prop="id" label="id" width="55">
								 	<template v-slot="scope">
            							<span>{{scope.$index+1}}</span>
        							</template>
						      </el-table-column>
						      <el-table-column prop="code" label="code" width="70">
									<template v-slot:default="scope">
            							<span>{{scope.row.symbol}}</span>
        							</template>
						      </el-table-column>
						      <el-table-column prop="name" label="name" width="80">
								  	<template v-slot:default="scope">
            							<span>{{scope.row.name}}</span>
        							</template>
						      </el-table-column>
							  <el-table-column prop="select" label="select" width="45">
      								<template v-slot:default="scope">
										<el-tooltip class="item" effect="light" :content=scope.row.hint 
											placement="right-start">
        									<el-button
          										size="mini" style="padding:3px; width:20px;font-size:14px;"
          										@click="handleBtn(scope.$index, scope.row.symbol, $event)">
											  	{{scope.row.btnname}}
											</el-button>
										</el-tooltip>
      								</template>
    						  </el-table-column>		
						    </el-table>
						</el-row>
					</el-aside>
					<el-main>
						<template>
  							<el-tabs v-model="activeCard" type="card" @tab-click="cardClick" id="thetabs">
    							<el-tab-pane label="K线图" name="kline">
									<div
										v-loading="klineLoading"
    									element-loading-text="正在从服务器获取K线数据..."
    									element-loading-background="rgba(0, 0, 0, 0.8)"
									>
										<!-- :klineParams="klineParams" :klineData="klineData" 绑定下面data数据 用于自定制数据传输到vue-kline, ref="callMethods"绑定一个DOM事件 用于调用接口  --->
    									<Vue-kline 
											:klineParams="klineParams" :klineData="klineData" ref="callMethods" 
											@refreshKlineData="refreshKlineData" 
											style="margin: auto">
										</Vue-kline>
									
									</div>
								</el-tab-pane>
    							<el-tab-pane label="配置管理" name="second" class="klinePane">配置管理

								</el-tab-pane>
    							<el-tab-pane label="角色管理" name="third">角色管理

								</el-tab-pane>
  							</el-tabs>
						</template>
					</el-main>
				</el-container>

			</el-main>
		</el-container>
		
	</div>
</template>

<script>
	import Vue from 'vue'
	import axios from 'axios'
	import VueAxios from 'vue-axios'
	import VueKline from "../kline/kline";
	import data from "@/assets/data";
	   
	export default {
		name: "mainpage",
		
		data() {
			 
			return {
				key: 0, //for update page purpose
				tabPosition: 'left',
				identifyCode: '1234',
				contentWidth: 110,
				slDialogTitle: 'Sign Up',
				dialogType: 'signup',
				tabledata:[],  //当前显示的股票列表
				stocklist: [], //所有股票列表
				btntype_sha: "",
				btntype_sza: "",
				btntype_zxb: "",
				btntype_kcb: "",
				btntype_cyb: "",
				btntype_zxg: "",
				activeCard: "kline",
				stockCode: "sh.600000", //当前选择的股票代码
				klineOption: 86400000, //当前k线类型，900000-15m, 86400000-1d
				stockListLoading: false,
				klineLoading: false,

				klineParams: {
        			width: 800,
        			height: 500,
        			theme: "dark",
        			language: "zh-cn",
        			ranges: ["1w", "1d", "1h", "30m", "15m", "5m", "line"],
        			symbol: "600000",
        			symbolName: "浦发银行",
        			intervalTime: 5000,
        			depthWidth: 50,
        			count: 1,
     			},
      			klineData: {}
			}
		},
		
		components: {
			VueKline
		},
				
		props: [], 
		
		mounted() {
			this.$nextTick(()=>{ // 页面渲染完成后的回调
				//以下操作是为了应用窗口变化时K线图能够自适应
				var width1 = document.getElementById("thetabs").offsetWidth - 10;
				var height1= document.getElementById("thetabs").offsetHeight - 70;

				//console.log("W:" + width1 + "H:" + height1);
				
				this.klineParams.width =width1;
				this.klineParams.height= height1;

				this.$refs.callMethods.resize(width1, height1); 
				//console.log("W:" + this.klineParams.width + "H:" + this.klineParams.height);
			})
	
			this.getstocklist()
			//this.handleUpdate()

			
		},
		
		
		methods: {
			//希望用于页面刷新，但好像没用
			handleUpdate() {
        		this.key += 1 
			},

			//获取KLine数据
			getKLineData(sCode, sFreq) {    
				//this.klineData = data;
	  			//this.$refs.callMethods.kline.chartMgr.getChart().updateDataAndDisplay(data.data.lines);
				this.klineLoading = true;
				  
				this.axios.get('/api/get_kline',
								{params: {"sCode": sCode, "sFreq": sFreq}}
				)
			    	.then((response) => {
			        	var res = response.data;

						this.klineLoading = false;

			        	if (res.error_num === 0) {
							this.klineData = response.data
							//this.klineData.data = response.data;
							
							this.$refs.callMethods.kline.chartMgr.getChart().updateDataAndDisplay(res.data.lines); //强制更改缓存中的lines值,防止显示不同步
							//console.log("line number:" + res.lines.length)
							
						}else {
			            	this.$message.error(res['msg'])
							console.log(res['msg'])
							//this.$router.push({path:'/'})
			    		}
					},
					(error)=>{
						this.klineLoading = false;

						this.$message.error(error.message)
						console.log(error.message)
					})

   			},

			refreshKlineData(option) {
				var klType = this.getKLineType(option);

				this.klineOption = option;

				console.log("KlineType: " + klType); //其他时间
				
				this.getKLineData(this.stockCode, klType);
			},

			getKLineType(msTime) {
				var klType = "15"

				if (msTime > 604800000) {
					klType = "m"
				} else if (msTime === 604800000){
					klType = "w"
				} else if (msTime === 86400000){
					klType = "d"
				} else if (msTime === 3600000){
					klType = "60"
				} else if (msTime === 1800000) {
					klType = "30"
				} else if (msTime === 900000) {
					klType = "15"
				} else if (msTime === 300000) {
					klType = "5"
				} else if (msTime === 60000) {
					klType = "1"
				}

				return klType
			},

			stockRowClick(row, column, event) {
				//var index = row.id - 1;
				var code = row.symbol;
				var ex = row.exchange;

				if (ex === "SSE") {
					code = "sh." + code
				}
				else{
					code = "sz." + code
				}

				//console.log("column: " + column.label)
				if ((this.stockCode != code) && (column.label != "select")) {
					this.$refs.callMethods.setSymbol(row.symbol, row.name);
					this.stockCode = code;
					//this.klineOption = 86400000; //当前k线类型，900000-15m, 86400000-1d
					this.refreshKlineData(this.klineOption);// 进入页面时执行,默认聚合时间900000毫秒(15分钟)
				}
				
			},

			//页面切换处理
			cardClick() {
        		this.handleUpdate() 
			},
			  
			//自选按钮处理
			handleBtn(index, symbol, event){
				var select = this.tabledata[index].selected
				var myindex=-1

				for (var row=0; row < this.stocklist.length; ++row) {
					if (this.stocklist[row].symbol === symbol){
						myindex = row
						break
					}
				}

				//console.log("row1:" + this.stocklist[myindex].symbol + this.stocklist[myindex].selected)

				if (select === "true"){
					this.save_selected(symbol, "false")
					
					this.tabledata[index].selected = "false"
					this.tabledata[index].btnname = "+"
					this.tabledata[index].hint = "加自选"
					//event.srcElement.innerHTML = "+"

					this.stocklist[myindex].selected = "false"
					this.stocklist[myindex].btnname = "+"
					this.stocklist[myindex].hint = "加自选"
					if (this.btntype_zxg === "primary") {
						this.tabledata = this.stocklist.filter(item=>{return ((item.selected === "true"))})
						//event.srcElement.innerHTML = "-"  //因为前面手动改为"加自选"就不能自动更新了
					}
				}
				else{
					var allselected = this.stocklist.filter(item=>{return ((item.selected === "true"))})

					if (allselected.length >= 20){
						this.$message({
									message: 'The maxium number of favorite stocks is 20',
									type: 'error'
							})
					}else{
						this.save_selected(symbol, "true")

						this.tabledata[index].selected = "true"
						this.tabledata[index].btnname = "-"
						this.tabledata[index].hint = "去自选"
						//event.srcElement.innerHTML = "-"

						this.stocklist[myindex].selected = "true"
						this.stocklist[myindex].btnname = "-"
						this.stocklist[myindex].hint = "去自选"
					}
				}
				
			},

			//保存自选
			save_selected: function(symbol, selected){

				this.axios.post("/api/save_selected/", 
					{"symbol": symbol, "selected": selected}, 
					{headers: {
								'Content-type': 'application/x-www-form-urlencoded',
								'X-CSRFToken': this.$cookies.get("csrftoken")												
							}
					}
				) 
				.then(
					(response)=>{
						var res = response.data
						if (res.error_num === 0) {
							this.$message({
									message: 'Save favorate successfully',
									type: 'success'
							})

						} 
						else {
							this.$message.error(res['msg'])
							console.log(res['msg'])

						}
					},
					(error)=>{
						this.$message.error(error.message)
						console.log(error.message)

					});

			},

			getbtntip(selected){
				if (selected === "true"){
					return "去自选"
				}
				else{
					return "加自选"
				}
			},

			//自选按钮切换
			getbtnname(selected){
				if (selected === "true"){
					return "-"
				}
				else{
					return "+"
				}
			},

			logout: function(){
				this.axios.post("/api/logout/", {}, {
					headers: {
								'Content-type': 'application/x-www-form-urlencoded',
								'X-CSRFToken': this.$cookies.get("csrftoken")												
							}
					}
				) 
				.then(
					(response)=>{
						var res = response.data
						if (res.error_num === 0) {
							this.$cookies.remove("user_id")
							this.$cookies.remove("user_name")
							this.$cookies.remove("is_login")
											
							this.$router.push({path:'/'})
						} 
						else {
							this.$message.error(res['msg'])
							console.log(res['msg'])
						}
					},
					(error)=>{
						console.log(error.message)
					});
			},

			selectstocktype(event){
				//console.log("button clicked")
				var value = event.srcElement.innerText
				this.changestocktype(value)

			},

			//设置表格行的样式
            rowstyle({row,rowIndex}){
				if (rowIndex%2 === 0) {
					//return 'background-color:#ecf5ff'
					return {'background-color': '#ecf5ff', 'height':'15px'}
				} else {
					return {'height':'15px'}
				}
            },

			getstocklist: function(){
				//
				this.stockListLoading = true

				this.axios.get('/api/get_stocklist')
			    	.then((response) => {

			        	var res = response.data
					
			        	if (res.error_num === 0) {
							this.stocklist = res.datalist
							//这里用 for (data in this.stocklist) 取出的data不对，不是一个object

							console.log("stocklist len:" + this.stocklist.length)

							//this.gettabledata()
							this.changestocktype("沪A")

							this.stockListLoading = false

							this.klineParams.symbol = "600000"
							this.klineParams.symbolName = "浦发银行"
							this.$refs.callMethods.setSymbol(this.klineParams.symbol, this.klineParams.symbolName)
							this.refreshKlineData(this.klineOption)
						}else {
							this.stockListLoading = false
			            	this.$message.error(res['msg'])
							console.log(res['msg'])
							this.$router.push({path:'/'})
			    		}
					},
					(error)=>{
						this.stockListLoading = false
						this.$message.error(error.message)
						console.log(error.message)

					})
			},

			gettabledata: function(stocktype) {
				//this.tabledata = this.stocklist.filter(item=>{return ((item.market === "主板") && (item.exchange==="SSE"))})
				//console.log("tabledata len:" + this.tabledata.length)
				if (stocktype === "沪A") {
					this.tabledata = this.stocklist.filter(item=>{return ((item.market === "主板") && (item.exchange==="SSE"))})
				}else if (stocktype === "深A"){
					this.tabledata = this.stocklist.filter(item=>{return ((item.market === "主板") && (item.exchange==="SZSE"))})
				}else if (stocktype === "中小"){
					this.tabledata = this.stocklist.filter(item=>{return ((item.market === "中小板"))})
				}else if (stocktype === "科创"){
					this.tabledata = this.stocklist.filter(item=>{return ((item.market === "科创板"))})
				}else if (stocktype === "创业"){
					this.tabledata = this.stocklist.filter(item=>{return ((item.market === "创业板"))})
				}else if (stocktype === "自选"){
					this.tabledata = this.stocklist.filter(item=>{return ((item.selected === "true"))})
				}

				//console.log("selected:" + this.tabledata[0].selected)
			},

			changestocktype: function(stocktype) {
				//console.log("changestocktype");
				
				//Clear all the buttons
				this.btntype_sha = ""
				this.btntype_sza = ""
				this.btntype_zxb = ""
				this.btntype_kcb = ""
				this.btntype_cyb = ""
				this.btntype_zxg = ""

				if (stocktype === "沪A") {
					this.btntype_sha = "primary"
				}else if (stocktype === "深A"){
					this.btntype_sza = "primary"
				}else if (stocktype === "中小"){
					this.btntype_zxb = "primary"
				}else if (stocktype === "科创"){
					this.btntype_kcb = "primary"
				}else if (stocktype === "创业"){
					this.btntype_cyb = "primary"
				}else if (stocktype === "自选"){
					this.btntype_zxg = "primary"
				}
				
				this.gettabledata(stocktype)
			}
			
		}
		
	}
</script>

<style>
	/*
	找到html标签、body标签，和挂载的标签
	都给他们统一设置样式
	*/
	html,
	body,
	#app,
	.el-container {
		/*设置内部填充为0，几个布局元素之间没有间距*/
		padding: 0px;
		/*外部间距也是如此设置*/
		margin: 0px;
		/*统一设置高度为100%*/
		height: 100%;
	}
	
	.el-main {
		padding: 0px;
		margin: 0px;
		height: 100%;
		
	}
	
	.el-link {
		font-size:12px;
	}

	.groupbutton {
		padding: 3px 6px;
		font-size:15px;
	}

	.background {
		background-image: url('../../static/images/background-cloth.png');
		background-position: left top;
		background-repeat: repeat;
	}

	.el-header,
	.el-footer {
		background-color: #fcfcf7;
		color: #838383;
		text-align: center;
		line-height: 50px;
		display: inline-flex;
		align-items: center;
		justify-content: space-between;
	}

	.el-aside {
		background-color: #e1ebf5;
		color: #7e7e7e;
		/*设置内部填充为0，几个布局元素之间没有间距*/
		padding: 0px;
		/*外部间距也是如此设置*/
		margin: 0px;
		/*统一设置高度为100%*/
		height: 100%;
	}

	body>.el-container {
		margin-bottom: 0px;
		margin-top: 0px;
	}

	.fRight {
		float: right;
		text-align: center;
		margin-right: 5px;
		/*本来希望按钮间有间隔，但不起作用 */
	}

	.font-Logo {
		text-align: center;
		letter-spacing: 3px;
		font-weight: 700;
		color: #014d94;
		text-shadow:
			1px 1px 0 #999695,
			2px 2px 0 #999695,
			3px 3px 2px #999695;
		/*4px 4px 0 #b4b0af; */
	}

	.buttonback	{
  		border-style:solid;
  		border-width:2px;
		border-color: rgba(169, 169, 169, 0.89);
  	}

	.klinediv	{
  		border-style:solid;
  		border-width:2px;
		border-color: rgba(238, 12, 12, 0.89);
		height: 100%;
		margin: 0px;
		padding: 0px;
  	}

	.klinePane	{
  		border-style:solid;
  		border-width:3px;
		border-color: rgba(2, 138, 148, 0.89);
		height: 100%;
		margin: 0px;
		padding: 0px;
  	}

	.el-tabs{
		background-color: #fcfcf7;
		height: 100%;
	}

	.el-tab-pane{
		background-color: #fcfcf7;
		height: 100%;
	}

	.el-tab-pane__content{
		background-color: #fcfcf7;
		height: 100%;
	}

	.Absolute-Center {
  		width: 90%;
  		height: 90%;
  		overflow: auto;
  		margin: 1px;
  		/*position: absolute;*/
  		top: 0; left: 0; bottom: 0; right: 0;
	}
</style>
