<template>
    <div>
        <!-- 面包屑导航区 -->
        <el-breadcrumb separator-class="el-icon-arrow-right" class="top_breadcrumb">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>日志管理</el-breadcrumb-item>
            <el-breadcrumb-item>日志查看</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 卡片视图区 -->
        <el-card>
            <el-row :gutter="20">
                <el-col :span="7">
                    <el-input placeholder="请输操作人" v-model="keyWord" clearable @clear="getLogList">
                        <el-button slot="append" icon="el-icon-search" @click="selectLog"></el-button>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-button  @click="getLogList">清除筛选</el-button>
                </el-col>
                <el-col :span="4">
                    <a class="el-button"  href="http://127.0.0.1:8000/api/meeting/logexport">导出日志</a>
                </el-col>
            </el-row>

            <!-- 会议室列表区 -->
            <el-table :data="logList" border stripe>
                <el-table-column type="index"></el-table-column>
                <el-table-column label="操作人" prop="person"></el-table-column>
                <el-table-column label="行为" prop="action"></el-table-column>
                <el-table-column label="操作时间" prop="time"></el-table-column>
            </el-table>

            <!-- 分页区域 -->
            <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="queryInfo.currentPage"
            :page-sizes="[5, 10, 15]"
            :page-size="queryInfo.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
            </el-pagination>
        </el-card>
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
            logList: [],
            total: 0,
            keyWord: '',
        }
    },
    created () {
        this.getLogList()
    },
    methods: {
        getLogList () {
            this.axios({
                method: 'get',
                params:this.queryInfo,
                url: 'http://127.0.0.1:8000/api/meeting/getLogList'
            }
            ).then(
                res=>{
                    this.total = res.data.total;
                    this.logList = res.data.logs;
                    // console.log(res);
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
            this.getLogList()
        },
        // 监听页码值改变的事件
        handleCurrentChange (newPage) {
            this.queryInfo.currentPage = newPage
            this.getLogList()
        },
        async selectLog () {
            if(this.keyWord==''){
                this.$message.warning('请输入待查询的关键词')
            }else{
                this.axios({
                method: 'GET',
                url: 'http://127.0.0.1:8000/api/meeting/searchLog',
                params:{
                    way: 'action',
                    keyword: this.keyWord
                }
            })
            .then(res=>{
                console.log(res);
                if(res.data.status == 1){
                    this.$message.warning(res.data.msg);
                    this.keyWord = '';
                }else{
                    this.logList = res.data.logs;
                    this.total = res.data.total;
                    this.$message.success(res.data.msg);
                    this.keyWord = '';
                }
            })
            .catch(err=>{
                console.log(err);
            });
            }            
        }
    }
}
</script>

<style lang="less" scoped>
.top_breadcrumb {
    margin-bottom: 10px;
}
</style>
