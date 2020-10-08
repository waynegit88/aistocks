<template>

	<div class="home" >

		<el-container style="height: 100%; width: 100%; position: absolute;" direction="vertical" id = "rootForm">
			<el-header class="shadow" style="height: 55px; opacity: 0.6;">
				<div>
					<el-button class="font-Logo" type="text" style="float:left; font-weight:bold; font-size:18px;">
						AIStocks
					</el-button>
				</div>
				<div>
					<el-button plain round class="fRight" @click="openSignupDialog">Sign Up</el-button>
					<el-button plain round class="fRight" @click="openLoginDialog">Login</el-button>
				</div>
			</el-header>
			<el-main>
				<div class="mainTitle">
					<h1 class="font-shadow-3D">Enjoy the Peace</h1>
				</div>

				<div class="myPicture">
					<img src="../../static/images/Stanley park.jpg" alt="The peace bay">
				</div>
			</el-main>
		</el-container>

		<!--Sign up and Login dialog -->
		<el-dialog :title="slDialogTitle" :visible.sync="slDialogVisible" width="30%" center @opened="openDialog" 
		                       @close="closeDialog('ruleForm')" id = "slDialog">
			<el-form :model="ruleForm" :rules="rules" ref="ruleForm">
				<el-form-item prop="username">
					<el-input maxlength="128" placeholder="请输入用户名" v-model="ruleForm.username">
						<i slot="prepend" class="el-icon-s-custom" />
					</el-input>
				</el-form-item>
				
				<template v-if = "dialogType==='login'">
				<el-form-item prop="password">
					<el-input maxlength="128" placeholder="请输入密码" v-model="ruleForm.password" show-password key="password">
						<i slot="prepend" class="el-icon-lock" />
					</el-input>
				</el-form-item>
				</template>
				<template v-else>
				<el-form-item prop="password1">
					<el-input maxlength="128" placeholder="请输入密码" v-model="ruleForm.password1" show-password key="password1">
						<i slot="prepend" class="el-icon-lock" />
					</el-input>
				</el-form-item>

				<el-form-item prop="password2">
					<el-input maxlength="128" placeholder="请再输一次密码" v-model="ruleForm.password2" show-password key="password2">
						<i slot="prepend" class="el-icon-lock" />
					</el-input>
				</el-form-item>

				<el-form-item prop="email">
					<el-input maxlength="128" placeholder="请输入邮件地址" v-model="ruleForm.email" key="email">
						<i slot="prepend" class="el-icon-message" />
					</el-input>
				</el-form-item>
				</template>
				
				<el-form-item prop="vcode">
					<el-row>
						<el-col :span="16">
							<!-- 注意：prop与input绑定的值一定要一致，否则验证规则中的value会报undefined，因为value即为绑定的input输入值 -->
							<el-input v-model="ruleForm.vcode" placeholder="请输入验证码" width="100px" key="vcodeinput">
								<i slot="prepend" class="el-icon-key" />
							</el-input>
						</el-col>

						<el-col :span="8" class="identifybox">
							<div @click="refreshCode('ruleForm')">
								<!-- 这里:identifyCode是为了更新验证码，:contentWidth是为了适应窗口宽度变化，
								    :key是为了刷新一下验证码，不然有时显示不出来，这是比较奇怪的问题，先这样解决-->
								<SIdentify :identifyCode="identifyCode" :contentWidth="contentWidth"  
								           :key="identifyCode"></SIdentify>
							</div>
						</el-col> 
					</el-row>
				</el-form-item>
			</el-form>

			<span slot="footer" class="dialog-footer">
				<el-button @click="slDialogVisible = false">取 消</el-button>
				<el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
			</span>
		</el-dialog>
		
	</div>
</template>

<script>
	//import Vue from 'vue'
	//import axios from 'axios'
	//import VueAxios from 'vue-axios'
	import SIdentify from '@/components/common/SIdentify'
	import {makeCode} from '@/commonjs/codemaker.js'
	import elementResizeDetectorMaker from 'element-resize-detector'
   
	export default {
		name: "home",
		
		data() {
			// 验证码自定义验证规则
			const validateVerifycode = (rule, value, callback) => {
			  if (value === '') {
				callback(new Error('请输入验证码'))
			  } else if (value !== this.identifyCode) {
				console.log('validateVerifycode:', value)
				callback(new Error('验证码不正确!'))
			  } else {
				callback()
			  }
			}
			
			// 密码自定义验证规则
			const validatePassword1 = (rule, value, callback) => {
			  if (value === '') {
				callback(new Error('请输入密码'))
			  } 
			  else {
				  if (this.ruleForm.password2 !== '') {
					this.$refs.ruleForm.validateField('password2');
				  }
					
				  callback()
			  }
			}
			
			// 密码自定义验证规则
			const validatePassword2 = (rule, value, callback) => {
			  if (value === '') {
				callback(new Error('请再输一次密码'))
			  } else if ((value !== this.ruleForm.password1) && (this.ruleForm.password1 !== '')) {
				callback(new Error('两次输入的密码必须一致!'))
			  } else {
				callback()
			  }
			}
			 
			return {
				slDialogVisible: false,
				identifyCode: '1234',
				contentWidth: 110,
				slDialogTitle: 'Sign Up',
				dialogType: 'signup',
				ruleForm: {  
					username: "",
					password: "",
					password1: "",
					password2: "",
					email: "",
					vcode: ""
				},
				rules: {  
					username: [{
							required: true,
							message: "请输入用户名",
							trigger: "blur"
						},
						{
							pattern: /^[0-9A-Za-z_]{4,15}$/,
							message: "用户名只能为4-15位字母数字及下划线",
							trigger: "blur"
						}
					],
					password: [
						{ required: true, message: "请输入密码", trigger: 'blur'},
						{ min: 6, message: '密码长度最少为6位', trigger: 'blur' }
					],
					password1: [
						{ required: true, trigger: 'blur', validator: validatePassword1 },
						{
							min: 6,
							message: '密码长度最少为6位',
							trigger: 'blur'
						}
					],
					password2: [
						{ required: true, trigger: 'blur', validator: validatePassword2 },
						{
							min: 6,
							message: '密码长度最少为6位',
							trigger: 'blur'
						}
					],
					email: [{
							required: true,
							message: "请输入邮箱",
							trigger: "blur"
						},
						{
							pattern: /^([0-9A-Za-z\-_\.]+)@([0-9a-z]+\.[a-z]{2,3}(\.[a-z]{2})?)$/g,
							message: "请输入正确的邮箱",
							trigger: "blur"
						}
					],
					vcode: [
					   { required: true, trigger: 'blur', validator: validateVerifycode }
					]
				}
			}
		},
		
		components: {
			SIdentify
		},
				
		props: [], 
		
		mounted() {
			
			//监听元素大小变化
			let erd = elementResizeDetectorMaker()
			
		    erd.listenTo(document.getElementById("slDialog"), (element)=>{
		   			var width = element.offsetWidth
		
					//change the width of SIdentify
					this.contentWidth = Math.floor(width * 0.075)
					this.refreshCode()  //这里主要是为了在改变大小后重画一下验证码
				}) 
				
			//console.log("Mounted: Home")
		},

		beforeCreate() {
			//console.log("BeforeCreate: Home")
		},
		
		created() {
			//console.log("Created: Home")

			this.get_token() //获取csrf_token
		},
		
		methods: {
			get_token: function(){
				/*
			    this.axios.get('http://127.0.0.1:8000/api/get_csrf', {
					params: {'id':'001'},
					headers: {'Access-Control-Allow-Origin': '*'}
				}) */
				this.axios.get('http://127.0.0.1:8000/api/get_csrf')
			        .then((response) => {
						//var res = JSON.parse(response.bodyText)
						//var res = JSON.parse(response.data)
						var res = response.data
			            if (res.error_num === 0) {
			                var csrf_token = res.token
							this.$cookies.set("csrftoken", csrf_token)
							//console.log("csrftoken:" + csrf_token)
			            } else {
			                this.$message.error('Getting token failed')
			                console.log(res['msg'])
			            }
			        }, error => {
						console.log('Error', error.message)
					})
			},
			  
			// 切换验证码
			refreshCode: function(){
				this.identifyCode = makeCode(4)
			},
			
			openDialog: function(){
				// 验证码初始化
				this.refreshCode()
			},
			
			closeDialog: function(formName) {
			      this.$refs[formName].resetFields()
			},
			
			openSignupDialog: function() {
				this.dialogType = "signup"
				this.slDialogTitle = 'Sign Up'
				this.slDialogVisible = true
			},
			
			openLoginDialog: function() {
				this.dialogType = "login"
				this.slDialogTitle = 'Login'
				this.slDialogVisible = true
			},
			
			//submit for signup dialog
			submitForm: function(formName){
				this.$refs[formName].validate(valid => {
				    if(valid){ //校验通过
						if (this.dialogType === "signup") {
							/*var mydata = {username: this.ruleForm.username, password: this.ruleForm.password1, email: this.ruleForm.email}*/
							this.axios.post("/api/add_user/", 
										{name: this.ruleForm.username, 
										 password: this.ruleForm.password1, 
										 email: this.ruleForm.email
										}, 
										{headers: {
											'Content-type': 'application/x-www-form-urlencoded',
											'X-CSRFToken': this.$cookies.get("csrftoken")}
										}
									  ) 
								.then(
									(response)=>{
										console.log(response); 
										var res = response.data
									          if (res.error_num === 0) {
												this.$message({
												          message: '注册用户成功，请登录。',
												          type: 'success'
												        });
														  
												this.slDialogVisible = false;
									          } else {
									            this.$message.error(res['msg'])
									            console.log(res['msg'])
									          }
									}, (error)=>{
										console.log(error.message)
									});
						}
						else { //for login
							var username = this.ruleForm.username
							var password = this.ruleForm.password
							//console.log("user:"+ username)

							this.axios.post("/api/login/", {
											name: username, 
										 	password: password, 
										}, {
											headers: {
												'Content-type': 'application/x-www-form-urlencoded',
												'X-CSRFToken': this.$cookies.get("csrftoken")												
											}
										}
									  ) 
								.then(
									(response)=>{
										//console.log(response); 
										//var res = JSON.parse(response.data)
										var res = response.data
									    if (res.error_num === 0) {
											this.$cookies.set("user_id", res.user_id)
											this.$cookies.set("user_name", res.user_name)
											this.$cookies.set("is_login", true)
											
											this.$message({message: '登录成功', type: 'success'});

											//console.log("Cookies:" + this.$cookies.keys().join("\n"))
														  
											this.slDialogVisible = false;
											
											this.$router.push({path:'/mainpage'})
									    } 
										else {
									        this.$message.error(res['msg'])
									        console.log(res['msg'])
									    }
									},
									(error)=>{
										console.log(error.message)
									});
						}
				    }
				})
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

	body,
	.el-main,
	.home {
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
		text-align: center;
		line-height: 200px;
	}

	body>.el-container {
		margin-bottom: 0px;
	}

	.mainTitle {
		text-align: center;
	}

	.myPicture {
		padding: 1%;
		position: relative;
	}

	.myPicture>img {
		width: 95%;
		height: auto;
		left: 0;
		top: 0;
		display: block;
		margin: 0 auto;
		/*是图片水平居中 */
		border-color: gray;
		border-style: solid;
		border-top-width: 1px;
		border-bottom-width: 1px;
		border-left-width: 1px;
		border-right-width: 1px;
	}

	.fRight {
		float: right;
		text-align: center;
		margin-right: 5px;
		/*本来希望按钮间有间隔，但不起作用 */
	}

	.font-shadow-3D {
		text-align: center;
		letter-spacing: 10px;
		font-weight: 700;
		color: #6d6d6a;
		text-shadow:
			1px 1px 0 #b4b0af,
			2px 2px 0 #b4b0af,
			3px 3px 2px #b4b0af;
		/*4px 4px 0 #b4b0af; */
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
</style>
