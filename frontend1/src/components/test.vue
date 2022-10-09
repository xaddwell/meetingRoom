<template>
<div>
    this is test!
    {{msg}}
    <el-button @click="getData">请求用户数据 </el-button>
    <div>
        <el-input v-model="username" placeholder="Please input username" clearable />
        <el-input v-model="password" type="password" placeholder="Please input password" show-password/>
        <el-input v-model="password1" type="password" placeholder="Please input password again" show-password/>
        <el-input v-model="phone" placeholder="Please input phone" clearable />
        <el-input v-model="email" placeholder="Please input email" clearable />
        <el-button @click="login">登录 </el-button><el-button @click="register">注册 </el-button>
    </div>
    <br/>
    <el-button @click="resetPassword">reset</el-button>
    <el-button @click="changePassword">change</el-button>
    <el-button @click="deleteUser">delete</el-button>
    
    <!-- {{xxx}} -->
    <br/>
    <ul>
        <li v-for="item in xxx" :key="item.username"> {{item.username}}</li>
    </ul>
    <img src="http://127.0.0.1:8000//media/user_img/andy.jpeg"  alt="头像" />
    <hr/>
    <el-upload
        class="upload-demo"
        ref="upload"
        action="http://127.0.0.1:8000/api/usr/uploadImg"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :data="{username:username}"
        :auto-upload="false">
        <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
    </el-upload>
</div>
  
</template>

<script>
export default {
    data(){
        return {
            msg:"123",
            xxx: "",
            username:"",
            password:"",
            password1:"",
            phone:"",
            email:"",
            
        }
    },
    methods:{
        getData(){
            this.axios({
                method:'get',
                url:"http://127.0.0.1:8000/api/usr/getUserList",
                
            }).then(res=>{
                console.log(res);
                this.xxx = res.data.users;
                // alert(typeof this.xxx)
            }).catch(err=>{
                // console.log(err);
                alert('请求错误！！')
            })
        },
        login(){
            this.axios({
                method:'post',
                url:"http://127.0.0.1:8000/api/usr/login",
                data: this.qs.stringify({
                    username: this.username,
                    password: this.password
                })
                
            }).then(res=>{
                console.log(res);
                alert(res.data.msg)
            }).catch(err=>{
                // console.log(err);
                alert('请求错误！！')
            });
        },
        register(){
            this.axios({
                method:'post',
                url:"http://127.0.0.1:8000/api/usr/register",
                data: this.qs.stringify({
                    username: this.username,
                    password: this.password,
                    phone:this.phone,
                    email: this.email
                })
                
            }).then(res=>{
                console.log(res);
                alert(res.data.msg)
            }).catch(err=>{
                // console.log(err);
                alert('请求错误！！')
            });
        },
        resetPassword(){
            this.axios({
                method:'post',
                url:"http://127.0.0.1:8000/api/usr/resetPassword",
                data: this.qs.stringify({
                    username: this.username
                })
            })
            .then(res=>{
                console.log(res);
            })
            .catch(error=>{
                console.log(error);
            });
        },
        changePassword(){
            this.axios({
                method:'post',
                url:"http://127.0.0.1:8000/api/usr/changePassword",
                data:this.qs.stringify({
                    username: this.username,
                    oldpassword: this.password,
                    newpassword: this.password1
                })
            })
            .then(res=>{
                console.log(res);
            })
            .catch(error=>{
                console.log(error);
            })
        },
        deleteUser(){
            this.axios({
                method:'post',
                url:"http://127.0.0.1:8000/api/usr/deleteUser",
                data:this.qs.stringify({
                    username: this.username
                })
            })
            .then(res=>{
                console.log(res);
            })
            .catch(error=>{
                console.log(error);
            })
        },
        submitUpload() {
            this.$refs.upload.submit();
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        }
    }

}
</script>

<style lang="less" scoped>

</style>