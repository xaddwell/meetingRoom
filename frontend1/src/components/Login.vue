<template>
  <div class="login_container">
        <div class="login_box">
            <!-- 头像区域 -->
            <div class="avatar_box">
                <img src="../assets/admin.png" alt="">
            </div>

            <!-- 登录表单区域 -->
            <el-form ref="loginFormRef" class="login_form" :rules="loginFormRules" :model="loginForm">
                <!-- 用户名 -->
                <el-form-item prop="username">
                    <el-input v-model="loginForm.username" prefix-icon="iconfont icon-user" placeholder="请输入登录名称" clearable></el-input>
                </el-form-item>
                <!-- 密码 -->
                <el-form-item prop="password">
                    <el-input v-model="loginForm.password" prefix-icon="iconfont icon-password" type="password" placeholder="请输入登录密码" show-password></el-input>
                </el-form-item>

				<el-form-item>
				<el-checkbox v-model="checkboxVal">管理员登录</el-checkbox>
				</el-form-item>
                <!-- 登录按钮 -->
                <el-form-item class="btns">
                    <el-button type="primary" @click="login">登录</el-button>
                    <el-button type="info" @click="resetLoginForm">重置</el-button>
                    <el-button type="primary" @click="toRegister">前往注册</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import {loginNameValidator} from '../assets/js/validator'
import Welcome from '../components/user/Welcome.vue'

export default {
    data () {
        return {
            // 登陆表单的数据绑定对象
            loginForm: {
                username: '',
                password: ''
            },
            // 这是表单的验证规则对象
            loginFormRules: {
                // 验证用户名是否合法
                username: [
                    { required: true, message: '请输入登录名称', trigger: 'blur' },
                    { min: 2, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
                    {validator:loginNameValidator, trigger: 'blur'}
                ],
                // 验证密码是否合法
                password: [
                    { required: true, message: '请输入登录密码', trigger: 'blur' },
                    { min: 5, max: 10, message: '密码长度在 5 到 10 个字符', trigger: 'blur' }
                ]
            },
			checkboxVal:false
        }
    },
    methods: {
        // 点击重置按钮，重置登录表单
        resetLoginForm () {
            this.$refs.loginFormRef.resetFields();
        },	
		login () {
			this.$refs.loginFormRef.validate((valid) => { //判断是否通过表但验证
				if (valid) {
					this.axios({  // 通过，后台发送数据
					method: 'post',
					url:"http://127.0.0.1:8000/api/usr/login",
					data: this.qs.stringify({
						username : this.loginForm.username,
						password: this.loginForm.password,
						isadmin: this.checkboxVal
					})
				}).then(res=>{
					// console.log(res);
					if(res.data.status == 1 || res.data.status == 2){
						this.$message.error({
							message:'账号或密码错误',
							duration:1500
						});
						this.resetLoginForm();
					}else if(res.data.status == 3){
						this.$message.warning({
							message: '账号权限不够',
							duration:1500
						})
					}else{
						this.$message({
						message: '登陆成功',
						type: 'success',
						duration:1500
						});
						window.sessionStorage.setItem('username', this.loginForm.username+'');
                        window.sessionStorage.setItem('userType',res.data.userType);
						// alert(this.loginForm.username);
						if(this.checkboxVal){
							this.$router.push('/home');
						}else{
							this.$router.push('/user_book');
						}
					}
			})
			.catch(err=>{
				console.log(err);
			})
				} else {//没有通过表单验证
					console.log('error submit!!');
					return false;
				}
				});
			
		},

        toRegister(){
            this.$router.replace('register');
        }
    },
}
</script>

<style lang="less" scoped>
.login_container{
    background-color: rgb(98, 107, 230);
    height: 100%;
    width: 100%;
    background: url('../assets/img/loginbg.jpeg');
}

.login_box{
    width: 450px;
    height: 320px;
    background-color: #fff;
    border-radius: 3px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.9;

    .avatar_box{
        height: 130px;
        width: 130px;
        background-color: #fff;
        border: 1px solid #eee;
        border-radius: 50%;
        padding: 10px;
        position: absolute;
        transform: translate(-50%, -50%);
        left: 50%;
        img{
            width: 100%;
            height: 100%;
            background-color: #eee;
            border-radius: 50%;
        }
    }
}

.login_form{
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
}

.btns{
    display: flex;
    justify-content: flex-end;
}
</style>
