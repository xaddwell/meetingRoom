<template>
  <el-container class="home-container">
    <!-- 头部区域 -->
    <el-header>
      <div>
        <img src="../../assets/meeting.png" alt />
        <span>会议室预约系统</span>
      </div>
	  <el-dropdown>
	    <span class="el-dropdown-link">
	      个人信息<i class="el-icon-arrow-down el-icon--right"></i>
	    </span>
	    <el-dropdown-menu slot="dropdown">
	      <el-dropdown-item @click.native="change_pwd()">更改密码</el-dropdown-item>
	      <el-dropdown-item @click.native="change_info()">更改个人信息</el-dropdown-item>
	    </el-dropdown-menu>
	  </el-dropdown>
	  <div>
      <el-button type="info" @click="manageend">管理端</el-button>
      <el-button type="info" @click="logout">退出</el-button>
    </div>
      
    </el-header>
    <!-- 页面主体区域 -->
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <!-- 侧边栏菜单区域 -->
        <el-menu :default-active="activePath" :router="true" :collapse-transition="false" :collapse="isCollapse" :unique-opened="true" background-color="#333744" text-color="#fff" active-text-color="#409eff">
          <!-- 一级菜单 -->
          <el-submenu :index="item.id + ''" v-for="item in menulist" :key="item.id">
            <!-- 一级菜单的模板 -->
            <template slot="title">
              <!-- 图标 -->
              <i :class="iconsObj[item.id]"></i>
              <!-- 文本 -->
              <span>{{ item.authName }}</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item @click="saveNavState('/' + subItem.path)" :index="'/' + subItem.path" v-for="subItem in item.children" :key="subItem.id">
                <template slot="title">
                    <!-- 图标 -->
                    <i :class="iconsObj[subItem.id]"></i>
                    <!-- 文本 -->
                    <span>{{ subItem.authName }}</span>
                </template>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <!-- 右侧内容 -->
      <el-main>
        <!-- 路由占位符 -->
        <router-view></router-view>
        <!-- 更改密码对话框 -->
        <el-dialog
        title="修改用户密码"
        :visible.sync="changePasswordVisible"
        width="50%"
        @close="changePasswordDialogClosed">
          <el-form :model="changePasswordFrom" :rules="changePasswordRules" ref="changePasswordRef" label-width="100px">
            <el-form-item label="旧密码" prop="oldpassword">
              <el-input v-model='changePasswordFrom.oldpassword' prefix-icon="iconfont icon-password" type="password" placeholder="请输入旧密码" show-password></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="newpassword1">
              <el-input v-model="changePasswordFrom.newpassword1" prefix-icon="iconfont icon-password" type="password" placeholder="请输入新密码" show-password></el-input>
            </el-form-item>
            <el-form-item label="确认新密码" prop="newpassword2">
              <el-input v-model="changePasswordFrom.newpassword2" prefix-icon="iconfont icon-password" type="password" placeholder="请确认新密码" show-password></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="changePasswordVisible = false">取消</el-button>
            <el-button type="primary" @click="changePassowrd">确 定</el-button>
          </span>
        </el-dialog>
        <!-- 更改个人信息对话框 -->
                <el-dialog
        title="修改个人信息"
        :visible.sync="changeinfoVisible"
        width="50%"
        @close="changeinfoDialogClosed">
          <el-form :model="changeinfoForm" :rules="changeinfoRules" ref="changeinfoRef" label-width="100px">
            <el-form-item label="用户名" prop="username">
              <el-input v-model='changeinfoForm.username' prefix-icon="iconfont icon-user"  disabled></el-input>
            </el-form-item>
            <el-form-item label="用户角色" prop="userType">
              <el-input v-model='changeinfoForm.usrType' prefix-icon="iconfont icon-rolejiaose"  disabled></el-input>
            </el-form-item>
            <el-form-item label="部门" prop="dept">
              <el-input v-model='changeinfoForm.deptName' prefix-icon="iconfont icon-department"  disabled></el-input>
            </el-form-item>
            <el-form-item label="联系方式" prop="phone">
              <el-input v-model='changeinfoForm.phone' prefix-icon="iconfont icon-phone"></el-input>
            </el-form-item>
            <el-form-item label="电子邮箱" prop="email">
              <el-input v-model='changeinfoForm.email' prefix-icon="iconfont icon-email"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="changeinfoVisible = false">取消</el-button>
            <el-button type="primary" @click="changeinfo">确 定</el-button>
          </span>
        </el-dialog>

      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
    data () {
        //定义两次密码是否相同的校验器
        var repasswordValidator = (rule, value, callback)=>{
                if(value !== this.changePasswordFrom.newpassword1){
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
            changePasswordVisible:false,
            changePasswordFrom:{
              oldpassword: '',
              newpassword1: '',
              newpassword2: ''
            },
            changePasswordRules:{
              oldpassword: [
                { required: true, message: '请输入旧密码', trigger: 'blur' },
                { min: 5, max: 10, message: '密码长度在 5 到 10 个字符', trigger: 'blur' }
              ],
              newpassword1: [
                { required: true, message: '请输入新密码', trigger: 'blur' },
                { min: 5, max: 10, message: '密码长度在 5 到 10 个字符', trigger: 'blur' }
              ],
              newpassword2: [
                { required: true, message: '请输入确认新密码', trigger: 'blur' },
                { min: 5, max: 10, message: '密码长度在 5 到 10 个字符', trigger: 'blur' },
                {validator:repasswordValidator, trigger:'blur'}
              ]
            },
            changeinfoVisible:false,
            changeinfoForm:{},
            changeinfoRules:{
              phone:[
                { required: true, message: '请输入联系号码', trigger: 'blur' },
                {validator:checkMobile, trigger:'blur'}
              ],
              email:[
                {validator: checkEmail, trigger:'blur'}
              ]
            },
            // 左侧菜单数据
            menulist: [{
			      id: 100,
			      authName: '会议统计信息',
			      path: 'null',
			      children: [
			        { id: 1002, authName: '会议统计会议', path: 'user_meetingStatisticHistory' }
			      ]
			      },
				{
                id: 101,
                authName: '申请会议室',
                path: 'null',
                children: [
                    { id: 1011, authName: '进行预约', path: 'user_book' },
                    { id: 1012, authName: '取消预约', path: 'user_cancelBook' }
                ]
                },
                {
                id: 102,
                authName: '预约进程/历史',
                path: 'null',
                children: [
                    { id: 1021, authName: '已通过', path: 'user_approved' },
                    { id: 1022, authName: '未通过', path: 'user_notApproved' },
                    { id: 1023, authName: '审核中', path: 'user_approving' },
                    { id: 1024, authName: '查看历史会议', path: 'user_history' }
                ]
                },
				],
            iconsObj: {
				        100: 'iconfont icon-statistics',
                101: 'iconfont icon-applyto',
                102: 'iconfont icon-appointment',
				        103: 'iconfont icon-baobiao',
                1002: 'iconfont icon-count4',
                1011: 'el-icon-circle-plus',
                1012: 'el-icon-error',
                1021: 'el-icon-folder-checked',
                1022: 'el-icon-folder-opened',
                1023: 'el-icon-loading',
                1024: 'el-icon-document-copy',
            },
            isCollapse: false,
            activePath: ''
        }
    },
    created () {
        this.activePath = window.sessionStorage.getItem('activePath')
    },
    methods: {
        logout () {
            window.sessionStorage.clear()
            this.$router.push('/login')
        },
        // 点击按钮,切换菜单的折叠与展开
        toggleCollapse () {
            this.isCollapse = !this.isCollapse
        },
        // 保存链接的激活状态
        saveNavState (activePath) {
          window.sessionStorage.setItem('activePath', activePath)
          this.activePath = activePath
        },
        change_pwd(){
          this.changePasswordVisible=true;
        },
        changePasswordDialogClosed(){
          this.$refs.changePasswordRef.resetFields();
        },
        changePassowrd(){
          this.$refs.changePasswordRef.validate(valid=>{
            if(valid){
              this.axios({
                method: 'post',
                url:'http://127.0.0.1:8000/api/usr/changePassword',
                data: this.qs.stringify({
                  username: window.sessionStorage.getItem('username'),
                  oldpassword: this.changePasswordFrom.oldpassword,
                  newpassword: this.changePasswordFrom.newpassword1
                })
              })
              .then(res=>{
                // console.log(res);
                if(res.data.status==1){
                  this.$message.error(res.data.msg);
                  this.$refs.changePasswordRef.resetFields();
                }else if(res.data.status == 0){
                  this.$message.success(res.data.msg);
                  this.changePasswordVisible = false;
                }
              })
              .catch(err=>{
                console.log(err);
              });
            }else{
              console.log('error submit!');
              return false;
            }
          });
        },
        change_info(){ // 获取用户信息并显示信息修改对话框
          this.axios(
            {
              method: 'get',
              url: 'http://127.0.0.1:8000/api/usr/searchUser',
              params:{
                way: 'username',
                keyword: window.sessionStorage.getItem('username'),
              }
            }
          )
          .then(res=>{
            // console.log(res);
            this.changeinfoForm = res.data.users[0]
          })
          .catch(err=>{
            console.log(err);
          });
          this.changeinfoVisible=true;
        },
        changeinfo(){ // 像后端发送信息修改请求
          this.$refs.changeinfoRef.validate(valid=>{
            if(valid){
              this.axios({
                method: 'get',
                url:'http://127.0.0.1:8000/api/usr/editUser',
                params:{
                  usr: this.changeinfoForm.username,
                  phone: this.changeinfoForm.phone,
                  usrType: this.changeinfoForm.usrType,
                  email: this.changeinfoForm.email,
                  manage: false,
                  username: window.sessionStorage.getItem('username'),
                }
              })
              .then(res=>{
                // console.log(res);
                if(res.data.status == 0){
                  this.$message.success(res.data.msg);
                  this.changeinfoVisible = false;
                }else{
                  this.$message.error(res.data.msg);
                }
              })
              .catch(err=>{
                console.log(err);
              })
            }else{
              console.log('error submit!');
              return false;
            }
          })
        },
        changeinfoDialogClosed(){
          this.$refs.changeinfoRef.resetFields();
        },
        manageend(){
          this.$router.push('/home');
        }
        
    }
}
</script>

<style lang="less" scoped>

.el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
	margin-right:10px;
  }
.el-icon-arrow-down {
    font-size: 12px;
}
	
.home-container {
  height: 100%;
}

.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  color: #fff;
  font-size: 20px;
  > div {
    display: flex;
    align-items: center;
    height: 100%;
    img {
      height: 100%;
    }
    span {
      margin-left: 15px;
    }
  }
}

.el-menu {
    border-right: 0;
}

.el-aside {
  background-color: #333744;

  .toggle-button {
      background-color: #4a5064;
      cursor: pointer;
      color: #fff;
      font-size: 10px;
      line-height: 24px;
      text-align: center;
      letter-spacing: .2em;
  }

  .el-main {
      border-right: 0;
  }
}

.iconfont {
    margin-right: 10px;
}
</style>
