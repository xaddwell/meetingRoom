<template>
    <div>
        <!-- 面包屑导航区 -->
        <el-breadcrumb separator-class="el-icon-arrow-right" class="top_breadcrumb">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>部门管理</el-breadcrumb-item>
            <el-breadcrumb-item>部门用户</el-breadcrumb-item>
        </el-breadcrumb>


        <el-tabs v-model="activeName">
            <el-tab-pane label="已分配部门" name="distributed">
                <!-- 卡片视图区 -->
                <el-card>
                    <el-row :gutter="20">
                        <el-col :span="5">
                            <el-select v-model="value" placeholder="请选择部门" @change="selectDeptUser(value)">
                                <el-option
                                v-for="item in deptList"
                                :key="item.deptNo"
                                :label="item.deptName"
                                :value="item.deptNo">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="7">
                            <el-input placeholder="请输关键词" v-model="keyWord" clearable @clear="getdistributedUserList">
                                <el-button slot="append" icon="el-icon-search" @click="selectDept"></el-button>
                            </el-input>
                        </el-col>
                        <el-col :span="4">
                            <el-button  @click="getdistributedUserList">清除筛选</el-button>
                        </el-col>
                    </el-row>

                    <!-- 会议室列表区 -->
                    <el-table :data="distributedList" border stripe>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="用户名" prop="username"></el-table-column>
                        <el-table-column label="用户角色" prop="usrType"></el-table-column>
                        <el-table-column label="部门">
                            <template slot-scope="scope">
                                <el-select v-model="scope.row.dept" placeholder="请选择" @change="deptchange(scope.row.username, scope.row.dept)">
                                    <el-option
                                    v-for="item in deptList"
                                    :key="item.deptNo"
                                    :label="item.deptName"
                                    :value="item.deptNo">
                                    </el-option>
                                </el-select>
                            </template>
                        </el-table-column>
                        <el-table-column label="联系号码" prop="phone"></el-table-column>
                        <el-table-column label="邮箱" prop="email"></el-table-column>
                        <el-table-column label="操作" width="180px">
                            <template slot-scope="scope">
                                <!-- 修改按钮 -->
                                <el-tooltip class="item" effect="dark" content="更多操作" placement="top" :enterable="false">
                                    <el-dropdown >
                                        <el-button type="primary" size="mini">
                                            ...<i class="el-icon-arrow-down el-icon--right"></i>
                                        </el-button>
                                        <el-dropdown-menu slot="dropdown">
                                            <el-dropdown-item @click.native="showEditDialog(scope.row.username)">修改用户信息</el-dropdown-item>
                                            <el-dropdown-item @click.native="resetUserpassword(scope.row.username)">重置用户密码</el-dropdown-item>
                                        </el-dropdown-menu>
                                    </el-dropdown>
                                </el-tooltip>
                                <!-- 删除按钮 -->
                                <el-tooltip class="item" effect="dark" content="删除用户" placement="top" :enterable="false">
                                    <el-button size="mini" type="danger" icon="el-icon-delete" @click="removeUserById(scope.row.username)"></el-button>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                    </el-table>

                    <!-- 分页区域 -->
                    <el-pagination
                    @size-change="handleSizeChangedistributed"
                    @current-change="handleCurrentChangedistributed"
                    :current-page="queryInfodistributed.currentPage"
                    :page-sizes="[5, 10, 15]"
                    :page-size="queryInfodistributed.pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="distributedtotal">
                    </el-pagination>
                </el-card>          
            </el-tab-pane>
            <el-tab-pane label="未分配部门" name="nodistributed">
                <!-- 卡片视图区 -->
                <el-card>
                    <el-row :gutter="20">
                        <el-col :span="7">
                            <el-input placeholder="请输关键词" v-model="keyWord" clearable @clear="getnodistributedUserList">
                                <el-button slot="append" icon="el-icon-search" @click="selectDept"></el-button>
                            </el-input>
                        </el-col>
                        <el-col :span="4">
                            <el-button  @click="getnodistributedUserList">清除筛选</el-button>
                        </el-col>
                    </el-row>

                    <!-- 会议室列表区 -->
                    <el-table :data="nodistributedList" border stripe>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="用户名" prop="username"></el-table-column>
                        <el-table-column label="用户角色" prop="usrType"></el-table-column>
                        <el-table-column label="部门">
                            <template slot-scope="scope">
                                <el-select v-model="scope.row.dept" placeholder="请选择" @change="deptchange(scope.row.username, scope.row.dept)">
                                    <el-option
                                    v-for="item in deptList"
                                    :key="item.deptNo"
                                    :label="item.deptName"
                                    :value="item.deptNo">
                                    </el-option>
                                </el-select>
                            </template>
                        </el-table-column>
                        <el-table-column label="联系号码" prop="phone"></el-table-column>
                        <el-table-column label="邮箱" prop="email"></el-table-column>
                        <el-table-column label="操作" width="180px">
                            <template slot-scope="scope">
                                <!-- 修改按钮 -->
                                <el-tooltip class="item" effect="dark" content="更多操作" placement="top" :enterable="false">
                                    <el-dropdown >
                                        <el-button type="primary" size="mini">
                                            ...<i class="el-icon-arrow-down el-icon--right"></i>
                                        </el-button>
                                        <el-dropdown-menu slot="dropdown">
                                            <el-dropdown-item @click.native="showEditDialog(scope.row.username)">修改用户信息</el-dropdown-item>
                                            <el-dropdown-item @click.native="resetUserpassword(scope.row.username)">重置用户密码</el-dropdown-item>
                                        </el-dropdown-menu>
                                    </el-dropdown>
                                </el-tooltip>
                                <!-- 删除按钮 -->
                                <el-tooltip class="item" effect="dark" content="删除用户" placement="top" :enterable="false">
                                    <el-button size="mini" type="danger" icon="el-icon-delete" @click="removeUserById(scope.row.username)"></el-button>
                                </el-tooltip>
                            </template>
                        </el-table-column>
                    </el-table>

                    <!-- 分页区域 -->
                    <el-pagination
                    @size-change="handleSizeChangenodistributed"
                    @current-change="handleCurrentChangenodistributed"
                    :current-page="queryInfonodistributed.currentPage"
                    :page-sizes="[5, 10, 15]"
                    :page-size="queryInfonodistributed.pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="nodistributedtotal">
                    </el-pagination>
                </el-card> 
            </el-tab-pane>

        </el-tabs>

        <!-- 修改用户信息对话框 -->
        <el-dialog
        title="修改用户信息"
        :visible.sync="editDialogVisible"
        width="50%"
        @close="editDialogClosed">
        <el-form :model="editForm" :rules="editFormRules" ref="editFormRef" label-width="100px">
            <el-form-item label="用户名" prop="username">
                <el-input v-model="editForm.username" disabled></el-input>
            </el-form-item>
            <el-form-item label="联系方式" prop="phone">
                <el-input v-model="editForm.phone"></el-input>
            </el-form-item>
            <el-form-item label="电子邮箱" prop="email">
                <el-input v-model="editForm.email"></el-input>
            </el-form-item>
            <el-form-item label="用户角色" prop="usrType">
                <el-select v-model="editForm.usrType">
                    <el-option value="管理员">管理员</el-option>
                    <el-option value="普通用户">普通用户</el-option>
                </el-select>
                <!-- <el-input v-model="editForm.usrType"></el-input> -->
            </el-form-item>
            
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="editDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="eidtRoom">确 定</el-button>
        </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data () {
        // 验证手机号
        var checkMobile = (rule, value, cb) => {
            const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|166|17[3678]|18[0-9]|14[57])[0-9]{8}$/
            if (regMobile.test(value)) {
                return cb()
            }
            cb(new Error('请输入格式正确的手机'))
        }
        return {
            activeName: 'distributed',
            queryInfodistributed: {
                currentPage: 1,
                pageSize: 5
            },
            queryInfonodistributed:{
                currentPage: 1,
                pageSize: 5
            },
            value: '',  // 表示当前选择的部门
            deptList: [],
            distributedList: [],
            nodistributedList: [],
            distributedtotal: 0,
            nodistributedtotal: 0,
            keyWord: '',
            addDialogVisible: false,
            editDialogVisible: false,
            editForm: {},
            editFormRules: {
                deptName: [
                    { required: true, message: '请输入部门名', trigger: 'blur' }
                ],
                phone: [
                    { required: true, message: '请输入手机号', trigger: 'blur' },
                    { validator: checkMobile, trigger: 'blur' }
                ]
            }
        }
    },
    created () {
        this.getnodistributedUserList();
        this.getDeptList();
    },
    methods: {
        async getDeptList () {
            this.axios({
                method: 'get',
                url:'http://127.0.0.1:8000/api/usr/getDeptList',
                params: {all: true}
            }).then(res=>{
                this.deptList = res.data.depts;
            }).catch(err=>{
                console.log(err);
            })
        },
        getdistributedUserList (dept) {
            this.axios({
                method: 'get',
                params: {
                    currentPage: this.queryInfodistributed.currentPage,
                    pageSize: this.queryInfodistributed.pageSize,
                    way: 'dept',
                    distribute:'yes',
                    dept: dept
                },
                url: 'http://127.0.0.1:8000/api/usr/getUserList'
            }
            ).then(
                res=>{
                    // console.log(res);
                    this.distributedtotal = res.data.total;
                    this.distributedList = res.data.users;
                }
            ).catch(
                err=>{
                    console.log(err);
                }
            ); 
        },
        getnodistributedUserList () {
            this.axios({
                method: 'get',
                params:{
                    currentPage: this.queryInfonodistributed.currentPage,
                    pageSize: this.queryInfonodistributed.pageSize,
                    way: 'dept',
                    distribute:'no'
                },
                url: 'http://127.0.0.1:8000/api/usr/getUserList'
            }
            ).then(
                res=>{
                    // console.log(res);
                    this.nodistributedtotal = res.data.total;
                    this.nodistributedList = res.data.users;
                }
            ).catch(
                err=>{
                    console.log(err);
                }
            ); 
        },
        // 监听pageSize改变的事情
        handleSizeChangedistributed (newSize) {
            this.queryInfodistributed.pageSize = newSize
            this.getdistributedUserList(this.value);
        },
        // 监听页码值改变的事件
        handleCurrentChangedistributed (newPage) {
            this.queryInfodistributed.currentPage = newPage
            this.getdistributedUserList(this.value);
        },
        // 监听pageSize改变的事情
        handleSizeChangenodistributed (newSize) {
            this.queryInfonodistributed.pageSize = newSize
            this.getnodistributedUserList()
        },
        // 监听页码值改变的事件
        handleCurrentChangenodistributed (newPage) {
            this.queryInfonodistributed.currentPage = newPage
            this.getnodistributedUserList()
        },
        selectDeptUser(value){  //选择已分配部门的数据
            this.getdistributedUserList(value);
        },
        async selectDept () {
            if(this.keyWord==''){
                this.$message.warning('请输入待查询的关键词')
            }else{
                this.axios({
                method: 'GET',
                url: 'http://127.0.0.1:8000/api/usr/searchUser',
                params:{
                    way: 'username',
                    keyword: this.keyWord,
                    distribute: this.activeName
                }
            })
            .then(res=>{
                if(res.data.status == 1){
                    this.$message.warning(res.data.msg);
                    this.keyWord = '';
                }else{
                    if(this.activeName == 'distributed'){
                        this.distributedList = res.data.users;
                        this.distributedtotal = res.data.total;
                    }else{
                        this.nodistributedList = res.data.users;
                        this.distributedtotal = res.data.total;
                    }
                    this.$message.success(res.data.msg);
                    this.keyWord = '';
                }
            })
            .catch(err=>{
                console.log(err);
            });
            }            
        },
        editDialogClosed () {
            this.$refs.editFormRef.resetFields()
        },
        async showEditDialog (id) {
            const{data:res} = await this.axios({
                method:'get',
                url:'http://127.0.0.1:8000/api/usr/searchUser',
                params:{
                    way: 'username',
                    keyword: id
                }
            }) 
            // console.log(res);
            this.editForm = res.users[0];
            this.editDialogVisible = true;
        },
        eidtRoom () {
            this.$refs.editFormRef.validate(valid=>{
                if (!valid) return 
                this.axios({
                    method:'put',
                    url:'http://127.0.0.1:8000/api/usr/editUser',
                    params:{
                        usr: this.editForm.username,
                        phone: this.editForm.phone,
                        email: this.editForm.email,
                        usrType: this.editForm.usrType,
                        username: window.sessionStorage.getItem('username')
                    }
                }).then(res=>{
                    if(res.data.status == 0){
                        this.$message.success(res.data.msg);
                        if(this.activeName == 'distributed'){// 刷新数据
                            this.getdistributedUserList(this.value);
                        }
                        else{
                            this.getnodistributedUserList();
                        }
                        this.editDialogVisible = false;
                    }else{
                        this.$message.error(res.data.msg);
                    }
                }).catch(err=>{
                    console.log(err);
                })
            });
        },
        async removeUserById (id) {
            const confirmResult = await this.$confirm('此操作将永久删除该用户, 是否继续?',
            '提示',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).catch(err => err)
            if (confirmResult !== 'confirm') {
                return this.$message.info('已取消删除')
            }
            await this.axios({
                method: 'delete',
                url: 'http://127.0.0.1:8000/api/usr/deleteUser',
                params: {usr: id, username: window.sessionStorage.getItem('username')}
            })
            .then(res=>{
                if(res.data.status == 0){
                    this.$message.success(res.data.msg);
                    if(this.activeName == 'distributed'){// 刷新数据
                        this.getdistributedUserList();
                    }
                    else{
                        this.getnodistributedUserList();
                    }
                    this.editDialogVisible = false;

                }else{
                    this.$message.error(res.data.msg);
                }
            })
            .catch(err=>{
                console.log(err);
            })
        },
        resetUserpassword(id){
            this.axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/api/usr/resetPassword',
                data: this.qs.stringify({
                    usr : id,
                    username: window.sessionStorage.getItem('username')
                })
            })
            .then(res=>{
                if(res.data.status == 0){
                    this.$message.success(res.data.msg);
                }else if(res.data.status == 1){
                    this.$message.error(res.data.msg);
                }
            })
            .catch(err=>{
                console.log(err);
            })
        },
        deptchange(id, value){
            this.axios({
                method: 'get',
                url:'http://127.0.0.1:8000/api/usr/changeUserDept',
                params:{
                    usr: id,
                    dept: value,
                    username: window.sessionStorage.getItem('username')
                }
            })
            .then(res=>{
                console.log(res);
                if(res.data.status == 0){
                    this.$message.success(res.data.msg);
                    if(this.activeName == 'distributed'){// 刷新数据
                        this.getdistributedUserList(this.value);
                    }
                    else{
                        this.getnodistributedUserList();
                    }
                }else{
                    this.$message.error(res.data.msg);
                }
            }).catch(err=>{
                console.log(err);
            })
        }
    }
}
</script>

<style lang="less" scoped>
.top_breadcrumb {
    margin-bottom: 10px;
}
</style>
