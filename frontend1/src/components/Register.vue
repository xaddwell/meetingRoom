<template>
  <div class="register_container">
        <div class="register_box">
            <!-- 头像区域 -->
            <div class="avatar_box">
                <img src="../assets/admin.png" alt="">
            </div>

            <!-- 注册表单区域 -->
            <el-form ref="registerFormRef" class="register_form" :rules="registerFormRules" :model="registerForm">
                <!-- 用户名 -->
                <el-form-item prop="username">
                    <el-input v-model="registerForm.username" prefix-icon="iconfont icon-user" placeholder="请输入用户名称" clearable></el-input>
                </el-form-item>
                <!-- 密码 -->
                <el-form-item prop="password">
                    <el-input v-model="registerForm.password" prefix-icon="iconfont icon-password" type="password" placeholder="请输入登录密码" show-password></el-input>
                </el-form-item>
                <!-- 密码1 -->
                <el-form-item prop="password1">
                    <el-input v-model="registerForm.password1" prefix-icon="iconfont icon-password" type="password" placeholder="请确认登录密码" show-password></el-input>
                </el-form-item>
                <!-- 电话号码 -->
                <el-form-item prop="phone">
                    <el-input v-model="registerForm.phone" prefix-icon="iconfont icon-phone"  placeholder="请输入联系号码" clearable></el-input>
                </el-form-item>
                <!-- 电子邮箱 -->
                <el-form-item prop="email">
                    <el-input v-model="registerForm.email" prefix-icon="iconfont icon-email"  placeholder="请输入联系邮箱" clearable></el-input>
                </el-form-item>
                <!-- 按钮组 -->
                <el-form-item class="btns">
                    <el-button type="primary" @click="register">注册</el-button>
                    <el-button type="info" @click="resetLoginForm">重置</el-button>
                    <el-button type="primary" @click="toLogin">返回登陆</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import {loginNameValidator} from '../assets/js/validator'
export default {
    data () {
        //定义两次密码是否相同的校验器
        var repasswordValidator = (rule, value, callback)=>{
                if(value !== this.registerForm.password){
                    callback(new Error("two password don'not match!"))
                }else{
                    callback();
                }
            }
        var checkMobile = (rule, value, cb) => {
            const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|166|17[3678]|18[0-9]|14[57])[0-9]{8}$/
            if (regMobile.test(value)) {
                return cb()
            }
            cb(new Error('请输入格式正确的手机'))
        }
        var checkEmail = (rule, value, cb) => {
            const reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            if (reg.test(value) || value == '') {
            cb()
            } else {
            cb(new Error('邮箱格式错误'))
            }
        }
        return {
            // 登陆表单的数据绑定对象
            registerForm: {
                username: '',
                password: '',
                password1: '',
                phone: '',
                email: ''
            },
            // 这是表单的验证规则对象
            registerFormRules: {
                // 验证用户名是否合法
                username: [
                    { required: true, message: '请输入登录名称', trigger: 'blur' },
                    { min: 2, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
                    {validator:loginNameValidator, trigger: 'blur'}
                ],
                // 验证密码是否合法
                password: [
                    { required: true, message: '请输入登录密码', trigger: 'blur' },
                    { min: 5, max: 20, message: '密码长度在 5 到 20 个字符', trigger: 'blur' }
                ],
                // 验证密码是否合法
                password1: [
                    { required: true, message: '请确认登录密码', trigger: 'blur' },
                    { min: 5, max: 20, message: '密码长度在 5 到 20 个字符', trigger: 'blur' },
                    {validator:repasswordValidator, trigger:'blur'}
                    
                ],
                // 验证电话是否合法
                phone: [
                    { required: true, message: '请输入联系号码', trigger: 'blur' },
                    { validator: checkMobile, trigger: 'blur' }
                ],
                email:[
                    { validator: checkEmail, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        // 点击重置按钮，重置登录表单
        resetLoginForm () {
            this.$refs.registerFormRef.resetFields()
        },
        register () {
            this.$refs.registerFormRef.validate((valid) => {
                if (valid) { // 判断注册表单是否通过验证
                    this.axios({ // 通过，向后台发送数据
                        method: 'post',
                        url:"http://127.0.0.1:8000/api/usr/register",
                        data: this.qs.stringify({
                            username : this.registerForm.username,
                            password: this.registerForm.password,
                            phone: this.registerForm.phone,
                            email: this.registerForm.email
                        })
                    }).then(res=>{
                        console.log(res);
                        if(res.data.status == 1){
                            this.$message({
                            message: '该用户名已存在',
                            type: 'warning',
                            duration:1500
                            });
                        }else{
                            this.$message({
                            message: '注册成功',
                            type: 'success',
                            duration:1500
                            });
                            this.$router.replace('login');
                        }
                    })
                    .catch(err=>{
                        console.log(err);
                    })
                } else {
                    console.log('error submit!!');
                    return false;
                }
                });
            
        },
        toLogin(){
            this.$router.replace('login');
        }
    }
}
</script>

<style lang="less" scoped>
.register_container{
    background-color: rgb(98, 107, 230);
    height: 100%;
    width: 100%;
    background: url('../assets/img/loginbg.jpeg');
}

.register_box{
    width: 450px;
    height: 480px;
    background-color: #fff;
    border-radius: 3px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    opacity: 0.9;
    margin-top: 40px;

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

.register_form{
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
