<template>
    <div>
        <!-- 面包屑导航区 -->
        <el-breadcrumb separator-class="el-icon-arrow-right" class="top_breadcrumb">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>会议室管理</el-breadcrumb-item>
            <el-breadcrumb-item>会议室信息</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 卡片视图区 -->
        <el-card>
            <el-row :gutter="20" style="margin-bottom: 10px">
                <el-col :span="7">
                    <el-input placeholder="请输入会议室号" v-model="keyWord" clearable @clear="getRoomList">
                        <el-button slot="append" icon="el-icon-search" @click="selectRoom"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button  @click="getRoomList">清除筛选</el-button>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" @click="addDialogVisible = true">添加会议室</el-button>
                </el-col>
            </el-row>

            <!-- 会议室列表区 -->
            <el-table :data="roomList" border stripe>
                <el-table-column type="index"></el-table-column>
                <el-table-column label="会议室号" prop="roomNo"></el-table-column>
                <el-table-column label="会议室名称" prop="roomName"></el-table-column>
                <el-table-column label="可容纳人数" prop="roomSize"></el-table-column>
                <el-table-column label="会议室状态" prop="roomStatus"></el-table-column>
                <el-table-column label="空调状态" prop="roomstatus">
                    <template slot-scope="scope">
                        <el-switch @change="airStatusChanged(scope.row)" v-model="scope.row.air"></el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="投影仪状态" prop="roomstatus">
                    <template slot-scope="scope">
                        <el-switch @change="projectorStatusChanged(scope.row)" v-model="scope.row.projector"></el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="180px">
                    <template slot-scope="scope">
                        <!-- 修改按钮 -->
                        <el-tooltip class="item" effect="dark" content="修改会议室信息" placement="top" :enterable="false">
                            <el-button size="mini" type="primary" icon="el-icon-edit" @click="showEditDialog(scope.row.roomNo)"></el-button>
                        </el-tooltip>
                        <!-- 删除按钮 -->
                        <el-tooltip class="item" effect="dark" content="删除会议室" placement="top" :enterable="false">
                            <el-button size="mini" type="danger" icon="el-icon-delete" @click="removeRoomById(scope.row.roomNo)"></el-button>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页区域 -->
            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="queryInfo.currentPage"
            :page-sizes="[5, 10,15]"
            :page-size="queryInfo.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
            </el-pagination>
        </el-card>

        <!-- 添加会议室对话框 -->
        <el-dialog
        title="添加会议室"
        :visible.sync="addDialogVisible"
        width="50%"
        @close="addDialogClosed">
        <el-form :model="addForm" :rules="addFormRules" ref="addFormRef" label-width="100px">
            <el-form-item label="会议室号" prop="roomNo">
                <el-input v-model="addForm.roomNo"></el-input>
            </el-form-item>
            <el-form-item label="会议室名称" prop="roomName">
                <el-input v-model="addForm.roomName"></el-input>
            </el-form-item>
            <el-form-item label="可容纳人数" prop="roomSize">
                <el-input type="number" v-model="addForm.roomSize"></el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
            <el-button @click="addDialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="addRoom">确 定</el-button>
        </span>
        </el-dialog>

        <!-- 修改会议室信息对话框 -->
        <el-dialog
        title="修改会议室信息"
        :visible.sync="editDialogVisible"
        width="50%"
        @close="editDialogClosed">
        <el-form :model="editForm" :rules="editFormRules" ref="editFormRef" label-width="100px">
            <el-form-item label="会议室号" prop="roomNo">
                <el-input v-model="editForm.roomNo" :disabled='true'></el-input>
            </el-form-item>
            <el-form-item label="会议室名称" prop="roomName">
                <el-input v-model="editForm.roomName"></el-input>
            </el-form-item>
            <el-form-item label="可容纳人数" prop="roomSize">
                <el-input type="number" v-model="editForm.roomSize"></el-input>
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
        return {
            queryInfo: {
                currentPage: 1,
                pageSize: 5
            },
            roomList: [],
            total: 0,
            keyWord: '',
            addDialogVisible: false,
            editDialogVisible: false,
            addForm: {
                roomNo: '',
                roomName: '',
                roomSize: 0
            },
            addFormRules: {
                roomNo: [
                    { required: true, message: '请输入会议室号', trigger: 'blur' },
                    { min: 3, max: 4, message: '会议室号长度在3~4个数字之间', trigger: 'blur' }
                ],
                roomName: [
                    { required: true, message: '请输入会议室名称', trigger: 'blur' },
                    { min: 3, max: 10, message: '会议室号名称长度在3~10个之间', trigger: 'blur' }
                ],
                roomSize: [
                    { required: true, message: '请输入可容纳人数', trigger: 'blur' }
                ]
            },
            editForm: {},
            editFormRules: {
                roomName: [
                    { required: true, message: '请输入会议室名称', trigger: 'blur' },
                    { min: 3, max: 10, message: '会议室号名称长度在3~10个之间', trigger: 'blur' }
                ],
                roomSize: [
                    { required: true, message: '请输入可容纳人数', trigger: 'blur' }
                ]
            }
        }
    },
    created () {
        this.getRoomList()
    },
    methods: {
        getRoomList () {
            this.axios({
                method: 'get',
                params:this.queryInfo,
                url: 'http://127.0.0.1:8000/api/meeting/getRoomList'
            }
            ).then(
                res=>{
                    // console.log(res);
                    this.total = res.data.total;
                    this.roomList = res.data.rooms
                }
            ).catch(
                err=>{
                    console.log(err);
                }
            );
        },
        // 监听pageSize改变的事情
        handleSizeChange (newSize) {
            this.queryInfo.pageSize = newSize
            this.getRoomList()
        },
        // 监听页码值改变的事件
        handleCurrentChange (newPage) {
            this.queryInfo.currentPage = newPage
            this.getRoomList()
        },
        // 监听switch状态
        async roomStatusChanged (roomInfo) {
            const { data: res } = await this.$http.put('/room', { roomId: roomInfo.roomId, roomStatus: roomInfo.roomStatus })
            if (res.code !== 100) {
                roomInfo.roomStatus = !roomInfo.roomStatus
                return this.$message.error('修改会议室状态失败！')
            } else {
                this.$message.success('修改会议室状态成功！')
            }
        },
        async airStatusChanged (roomInfo) {
            // console.log(roomInfo.projector);
            const {data: res} = await this.axios({
                method: 'put',
                url: 'http://127.0.0.1:8000/api/meeting/devicechange',
                params:{
                    info: roomInfo.air,
                    device: 'air',
                    roomId: roomInfo.roomNo,
                    username: window.sessionStorage.getItem('username')
                }
            });
            // console.log(res);
            if (res.status == 0){
                this.$message.success(res.msg);
            }else{
                this.$message.error(res.msg);
            }
        },
        async projectorStatusChanged (roomInfo) {
            // console.log(roomInfo.projector);
            const {data: res} = await this.axios({
                method: 'put',
                url: 'http://127.0.0.1:8000/api/meeting/devicechange',
                params:{
                    info: roomInfo.projector,
                    device: 'projector',
                    roomId: roomInfo.roomNo,
                    username: window.sessionStorage.getItem('username')
                }
            });
            // console.log(res);
            if (res.status == 0){
                this.$message.success(res.msg);
            }else{
                this.$message.error(res.msg);
            }
        },
        selectRoom () {
            if(this.keyWord==''){
                this.$message.warning('请输入待查询的会议室号')
            }else{
                this.axios({
                method: 'GET',
                url: 'http://127.0.0.1:8000/api/meeting/searchRoom',
                params:{
                    way: 'roomId',
                    keyword: this.keyWord
                }
            })
            .then(res=>{
                if(res.data.status == 1){
                    this.$message.warning('请输入有效的会议室号');
                    this.keyWord = '';
                }else{
                    // console.log(res);
                    this.roomList = res.data.rooms;
                    this.total = res.data.total;
                    this.$message.success('查询会议室信息成功！');
                    this.keyWord = '';
                }
            })
            .catch(err=>{
                console.log(err);
            });
            }
        },
        addDialogClosed () {
            this.$refs.addFormRef.resetFields()
        },
        editDialogClosed () {
            this.$refs.editFormRef.resetFields()
        },
        addRoom () {
            this.$refs.addFormRef.validate((valid) => { //判断是否通过表但验证
                if (valid) {
                    this.axios({
                        method: 'post',
                        url: 'http://127.0.0.1:8000/api/meeting/addMeetingRoom',
                        data: this.qs.stringify({
                            roomNo: this.addForm.roomNo,
                            roomName: this.addForm.roomName,
                            roomSize: this.addForm.roomSize,
                            username: window.sessionStorage.getItem('username')
                        })
                    })
                    .then(res=>{
                        // console.log(res);
                        if(res.data.status == 1){  // 该会议室编号已存在
                            this.$message.error({
                                message: res.data.msg,
                                duration: 1500
                            })
                        }else{
                            this.$message.success({
                                message: res.data.msg,
                                duration: 1500
                            });
                            this.addDialogVisible = false;
                            this.getRoomList();
                        }
                    })
                    .catch(err=>{
                        console.log(err);
                    });
                } else {//没有通过表单验证
                    console.log('error submit!!');
                    return false;
                }
                });
        },
        async showEditDialog (id) {
            const {data : res} = await this.axios({
                method: 'get',
                url:'http://127.0.0.1:8000/api/meeting/searchRoom',
                params:{ 
                    way: 'roomId',
                    keyword: id
                }
            })
            // console.log(res);
            this.editForm = res.rooms[0];
            this.editDialogVisible = true;
        },
        eidtRoom () {
            this.$refs.editFormRef.validate(valid => {
                if (!valid) return
                this.axios({
                    method:'put',
                    url: 'http://127.0.0.1:8000/api/meeting/editRoom',
                    params: {
                        roomNo: this.editForm.roomNo,
                        roomName: this.editForm.roomName,
                        roomSize: this.editForm.roomSize,
                        username: window.sessionStorage.getItem('username')
                    }
                }).then(res=>{
                    // console.log(res);
                    if(res.data.status == 0){
                        this.$message.success(res.data.msg);
                        this.getRoomList();  // 刷新数据
                        this.editDialogVisible = false;
                    }else{
                        this.$message.error(res.data.msg);
                    }
                }).catch(err=>{
                    console.log(err);
                })
            })
        },
        async removeRoomById (id) {
            const confirmResult = await this.$confirm('此操作将永久删除该会议室, 是否继续?',
            '提示',
            {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).catch(err => err)
            // alert(confirmResult);
            if (confirmResult !== 'confirm') {
                this.$message.info('已取消删除')
                // alert(id)
                return 
            }
            await this.axios({
                method: 'delete',
                url:'http://127.0.0.1:8000/api/meeting/deleteRoom',
                params:{roomId: id, username: window.sessionStorage.getItem('username')}
            })
            .then(res=>{
                if(res.data.status == 0){
                    this.$message.success(res.data.msg)
                }else{
                    this.$message.error(res.data.msg)
                }
            })
            .catch(err=>{
                console.log(err);
            })

            this.getRoomList()
        }
    }
}
</script>

<style lang="less" scoped>
.top_breadcrumb {
    margin-bottom: 10px;
}

</style>
