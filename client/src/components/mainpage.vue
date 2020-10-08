<template>

	<div class="mainpage" >

		<el-container style="height: 100%; width: 100%; position: absolute;" direction="vertical" id = "rootForm">
			<el-header class="shadow background" style="height: 55px; opacity: 0.6;">
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
						    <el-table :data="tabledata" style="width: 100%; font-size:12px;" :show-header=false 
								:row-style="rowstyle" :cell-style="{padding:'0px'}">
						      <el-table-column prop="id" label="id" width="50">
								 	<template v-slot="scope">
            							<span>{{scope.$index+1}}</span>
        							</template>
						      </el-table-column>
						      <el-table-column prop="code" label="code" width="65">
									<template v-slot:default="scope">
            							<span>{{scope.row.symbol}}</span>
        							</template>
						      </el-table-column>
						      <el-table-column prop="name" label="name" width="70">
								  	<template v-slot:default="scope">
            							<span>{{scope.row.name}}</span>
        							</template>
						      </el-table-column>
							  <el-table-column prop="select" label="select" width="53">
      								<template v-slot:default="scope">
        								<el-button
          									size="mini" style="padding: 3px"
          									@click="handleBtn(scope.$index, scope.row.symbol, $event)">
											  {{getbtnname(scope.row.selected)}}
										</el-button>
      								</template>
    						  </el-table-column>		
						    </el-table>
						</el-row>
					</el-aside>
					<el-main>Main
					
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
	   
	export default {
		name: "mainpage",
		
		data() {
			 
			return {
				tabPosition: 'left',
				identifyCode: '1234',
				contentWidth: 110,
				slDialogTitle: 'Sign Up',
				dialogType: 'signup',
				//stocktype: "沪A",
				tabledata:[],
				stocklist: [],
				btntype_sha: "",
				btntype_sza: "",
				btntype_zxb: "",
				btntype_kcb: "",
				btntype_cyb: "",
				btntype_zxg: "",
			}
		},
		
		components: {
			
		},
				
		props: [], 
		
		mounted() {
			this.getstocklist()
		},
		
		
		methods: {
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
					event.srcElement.innerHTML = "加自选"

					this.stocklist[myindex].selected = "false"
					if (this.btntype_zxg === "primary") {
						this.tabledata = this.stocklist.filter(item=>{return ((item.selected === "true"))})
						event.srcElement.innerHTML = "去自选"  //因为前面手动改为"加自选"就不能自动更新了
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
						event.srcElement.innerHTML = "去自选"

						this.stocklist[myindex].selected = "true"
						
					}
				}
				
				//console.log("type:" + typeof(select))
				//console.log("selected:" + this.tabledata[index].selected)
				//console.log("row2:" + this.stocklist[myindex].symbol + this.stocklist[myindex].selected)
			},

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

			getbtnname(selected){
				if (selected === "true"){
					return "去自选"
				}
				else{
					return "加自选"
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
				this.axios.get('/api/get_stocklist')
			    	.then((response) => {
			        	var res = response.data
					
			        	if (res.error_num === 0) {
							this.stocklist = res.datalist
							//这里用 for (data in this.stocklist) 取出的data不对，不是一个object

							console.log("stocklist len:" + this.stocklist.length)

							//this.gettabledata()
							this.changestocktype("沪A")
							
			        	}else if (res.error_num === 1001) {
							this.$message.error(res['msg'])
							this.$router.push({path:'/'})			
						}else {
			            	this.$message.error(res['msg'])
							console.log(res['msg'])
							this.$router.push({path:'/'})
			    		}
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
</style>
