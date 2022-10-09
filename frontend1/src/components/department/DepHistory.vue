<template>
    <div>
        <!-- 面包屑导航区 -->
        <el-breadcrumb separator-class="el-icon-arrow-right" class="top_breadcrumb">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>部门管理</el-breadcrumb-item>
            <el-breadcrumb-item>部门历史会议</el-breadcrumb-item>
        </el-breadcrumb>

        <el-card>
            <!-- 头部警告区域 -->
            <el-alert show-icon :closable="false" title="注意：只有通过审批的会议才会加入到历史会议中！" type="warning"></el-alert>
            <el-select v-model="value" placeholder="请选择部门" @change="selectDept(value)">
                <el-option
                v-for="item in deptList"
                :key="item.deptNo"
                :label="item.deptName"
                :value="item.deptNo">
                </el-option>
            </el-select>

            <!-- tab标签页 -->
            <el-tabs v-model="activeName">
                <el-tab-pane label="已进行的会议" name="done">
                    <el-table :data="DoneList" border stripe>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="申请部门" prop="deptName" width="85"></el-table-column>
                        <el-table-column label="会议室" prop="roomNo"></el-table-column>
                        <el-table-column label="参会人数" prop="meetingSize"></el-table-column>
                        <el-table-column label="会议主题" prop="meetingTheme"></el-table-column>
                        <el-table-column label="开会日期">
                            <template slot-scope="scope">
                                <div>
                                    {{scope.row.meetingDate}}
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column label="开会时间">
                            <template slot-scope="scope">
                                <div v-if="scope.row.meetingSlot == 1">9:00-10:30</div>
                                <div v-if="scope.row.meetingSlot == 2">10:30-12:00</div>
                                <div v-if="scope.row.meetingSlot == 3">13:00-15:00</div>
                                <div v-if="scope.row.meetingSlot == 4">15:00-17:00</div>
                                <div v-if="scope.row.meetingSlot == 5">17:00-19:00</div>
                            </template>
                        </el-table-column>
                    </el-table>

                    <!-- 分页区域 -->
                    <el-pagination
                    @size-change="handleSizeChangeDone"
                    @current-change="handleCurrentChangeDone"
                    :current-page="queryDone.currentPage"
                    :page-sizes="[2, 4, 8, 10]"
                    :page-size="queryDone.pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="doneTotal">
                    </el-pagination>
                </el-tab-pane>
                <el-tab-pane label="未进行的会议" name="notdone">
                    <el-table :data="NotDoneList" border stripe>
                        <el-table-column type="index"></el-table-column>
                        <el-table-column label="申请部门" prop="deptName" width="85"></el-table-column>
                        <el-table-column label="会议室" prop="roomNo"></el-table-column>
                        <el-table-column label="参会人数" prop="meetingSize"></el-table-column>
                        <el-table-column label="会议主题" prop="meetingTheme"></el-table-column>
                        <el-table-column label="开会日期">
                            <template slot-scope="scope">
                                <div>
                                    {{scope.row.meetingDate}}
                                </div>
                            </template>
                        </el-table-column>
                        <el-table-column label="开会时间">
                            <template slot-scope="scope">
                                <div v-if="scope.row.meetingSlot == 1">9:00-10:30</div>
                                <div v-if="scope.row.meetingSlot == 2">10:30-12:00</div>
                                <div v-if="scope.row.meetingSlot == 3">13:00-15:00</div>
                                <div v-if="scope.row.meetingSlot == 4">15:00-17:00</div>
                                <div v-if="scope.row.meetingSlot == 5">17:00-19:00</div>
                            </template>
                        </el-table-column>
                    </el-table>

                    <!-- 分页区域 -->
                    <el-pagination
                    @size-change="handleSizeChangeNotDone"
                    @current-change="handleCurrentChangeNotDone"
                    :current-page="queryNotDone.currentPage"
                    :page-sizes="[2, 4, 8, 10]"
                    :page-size="queryNotDone.pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="notDoneTotal">
                    </el-pagination>
                </el-tab-pane>
            </el-tabs>
        </el-card>
    </div>
</template>

<script>
export default {
    data () {
        return {
            deptList: [],
            value: '',
            DoneList: [],
            NotDoneList: [],
            activeName: 'done',
            queryDone: {
                pageSize: 4,
                currentPage: 1,
                pass: 1,
				username:window.sessionStorage.getItem('username'),
				deptId:0
            },
            queryNotDone: {
                pageSize: 4,
                currentPage: 1,
                pass: 0,
				username:window.sessionStorage.getItem('username'),
				deptId:0
            },
            doneTotal: 0,
            notDoneTotal: 0
        }
    },
    created () {
        this.getDeptList()
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
        async selectDept (id) {
            this.queryDone.deptId = id
            this.queryNotDone.deptId = id
            const { data: resDone } = await this.axios({
				method:'get',
				url:'http://127.0.0.1:8000/meeting/selectDept',
				params:this.queryDone
			})
            if (resDone.code !== 100) {
                return this.$message.error('获取历史会议列表失败！')
            } else {
                this.DoneList = resDone.extend.result.list
                this.doneTotal = resDone.extend.result.total
            }
            const { data: resNotDone } = await this.axios({
            	method:'get',
            	url:'http://127.0.0.1:8000/meeting/selectDept',
            	params:this.queryNotDone
            })
            if (resNotDone.code !== 100) {
                return this.$message.error('获取历史会议列表失败！')
            } else {
                this.NotDoneList = resNotDone.extend.result.list
                this.notDoneTotal = resNotDone.extend.result.total
            }
        },
        handleSizeChangeDone (newSize) {
            this.queryDone.pageSize = newSize
            this.getDeptList()
        },
        handleCurrentChangeDone (newPage) {
            this.queryDone.currentPage = newPage
            this.getDeptList()
        },
        handleSizeChangeNotDone (newSize) {
            this.queryNotDone.pageSize = newSize
            this.getDeptList()
        },
        handleCurrentChangeNotDone (newPage) {
            this.queryNotDone.currentPage = newPage
            this.getDeptList()
        }
    }
}
</script>

<style lang="less" scoped>
    .el-select {
        margin-top: 15px;
    }

    .el-tabs {
        margin-top: 15px;
    }
    .top_breadcrumb {
    margin-bottom: 10px;
}
</style>
