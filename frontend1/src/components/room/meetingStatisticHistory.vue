<template>
  <div>
    <Row :gutter="26">
      <Col span="6">
        <Card class="meeting">
          <Icon type="ios-calendar" color="white"/>
          <h2>
            <b>{{todayMeetings.length}}</b>
          </h2>
          <h5 className="text-muted">今日会议</h5>
        </Card>
      </Col>
      <Col span="6">
        <Card class="meetingRoom">
          <Icon type="ios-bookmarks" color="white"/>
          <h2>
            <b>{{meetings.length}}</b>
          </h2>
          <h5 className="text-muted">已预定会议</h5>
        </Card>
      </Col>
      <Col span="6">
        <Card class="bookedMeeting">
          <Icon type="md-chatboxes" color="white"/>
          <h2>
            <b>{{totalMeetings.length}}</b>
          </h2>
          <h5 className="text-muted">全部会议</h5>
        </Card>
      </Col>
      <Col span="6">
        <Card class="todayMeeting">
          <Icon type="ios-easel" color="white"/>
          <h2>
            <b>{{totalMeetingRooms.length}}</b>
          </h2>
          <h5 className="text-muted">会议室总数</h5>
        </Card>
      </Col>
    </Row>
    <Row :gutter="26">
      <Col span="8">
        <Card style="margin-top: 20px; height: 333px">
          <div v-if="meetings.length !== 0" style="margin-top: 20px;margin-left: 40px">
            <TimelineItem v-for="(meeting, meetingId) in meetings" :key="meetingId" color="green">
              <p class="time">{{meeting.meetingDate}}&nbsp;&nbsp;{{meeting.meetingStartTime}}--{{meeting.meetingEndTime}}</p>
              <p class="content">会议主题：{{meeting.meetingTopic}}</p>
              <p class="content">会议室：{{meeting.meetingRoomName}}</p>
            </TimelineItem>
          </div>
          <div v-else style="margin: 123px 20px">
            <TimelineItem>
              <p class="time">暂时没有数据</p>
            </TimelineItem>
          </div>
        </Card>
      </Col>
      <Col span="6">
        <Card style="margin-top: 20px;height: 333px">
          <Calendar v-on:choseDay="clickDay">
          </Calendar>
        </Card>
      </Col>
      <Col span="10">
        <Card style="margin-top: 20px">
          <div id="room" :style="{width: '100%', height: '300px'}"></div>
        </Card>
      </Col>
    </Row>
    <Row :gutter="26">
      <Col span="26">
        <Card style="margin-top: 20px">
          <div id="meetingRoom" :style="{width: '100%', height: '400px'}"></div>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script>
  import {QueryAllMeetings, QueryMeetingForUser} from "../../api/meeting"
  import {QueryAllRoom,QuerymyRoomChartoption,QuerymyChartoption} from "../../api/meeting";
  import Calendar from "vue-calendar-component";

  export default {
    name: 'Home',
    data() {
      return {
        userId: '',
        todayMeetings: [],
        meetings: [],
        data: '',
        totalMeetings: [],
        totalMeetingRooms: [],
		myRoomChartoption:{series:[{data: [10, 2, 10, 11, 50, 5, 8]}],},
		myChartoption:{series:[{data: [{value: 335, name: '测试会议室1'}, {value: 335, name: '测试会议室2'},{value: 335, name: '测试会议室3'}]}],},
		
	  }
	},
    components: {
      Calendar
    },
    methods: {
      queryAllMeetings() {
        return new Promise(((resolve, reject) => {
          QueryAllMeetings().then(response => {
			  this.totalMeetings = response.data;
			  });
        }))
      },

      queryAllRoom() {
        return new Promise(((resolve, reject) => {
          QueryAllRoom().then(response => this.totalMeetingRooms = response.data);
        }))
      },
	  querymyRoomChartoption() {
	    return new Promise(((resolve, reject) => {
	      QuerymyRoomChartoption().then(response => this.myRoomChartoption = response);
	    }))
	  },
	  querymyChartoption() {
	    return new Promise(((resolve, reject) => {
	      QuerymyChartoption().then(response => this.myChartoption = response);
	    }))
	  },

      queryMeetingForUser() {
        return new Promise((resolve, reject) => {
          QueryMeetingForUser().then(response => {
            let todayMeeting = [];
            this.meetings = response.data;
            response.data.forEach(item => {
              if (item.meetingDate.substring(6,10) === this.data.substring(5,9)) {
                todayMeeting.push(item);
              }
            });
            this.todayMeetings = todayMeeting;
          })
        })
      },

      clickDay(data) {
        console.log(data);
        this.data = data.replace(/\//g, '-');
        this.queryMeetingForUser();
      },
	  
	  setChartOption(){
		  let myRoomChart = this.$echarts.init(document.getElementById('meetingRoom'));
		  let myChart = this.$echarts.init(document.getElementById('room'));
		  myRoomChart.setOption(myRoomChartoption);
		  myChart.setOption(myChartoption);
	  },

      drawMeetingRoom() {
        let myRoomChart = this.$echarts.init(document.getElementById('meetingRoom'));
        myRoomChart.setOption({
          title: {
            text: '会议室预定情况',
            x: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['会议室预订数']
          },
          calculable: true,
          xAxis: [
            {
              type: 'category',
              boundaryGap: false,
              data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            }
          ],
          yAxis: [
            {
              type: 'value',
              axisLabel: {
                formatter: '{value}'
              }
            }
          ],
          series: [
            {
              name: '会议室预定数',
              type: 'line',
              data: [1, 2, 10, 11, 1, 5, 8],
              markPoint: {
                data: [
                  {type: 'max', name: '最大值'},
                  {type: 'min', name: '最小值'}
                ]
              },
              markLine: {
                data: [
                  {type: 'average', name: '平均值'}
                ]
              }
            }
          ]
        })
      },

      drawRoom() {
        let myChart = this.$echarts.init(document.getElementById('room'));
        myChart.setOption({
          title: {
            text: '会议室占用比例',
            x: 'center'
          },
          tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
          },
          calculable: true,
          series: [
            {
              name: '会议室占用比例',
              type: 'pie',
              radius: '55%',
              center: ['50%', '60%'],
              data: [
                {value: 335, name: '测试会议室3'},
                {value: 310, name: '测试会议室4'},
                {value: 234, name: 'MeetingRoom1'},
                {value: 135, name: 'MeetingRoom2'}
              ]
            }
          ]
        });
      }
    },
    mounted() {
      // this.userId = this.$store.state.user.userId;
      let myDate = new Date();
      this.data = myDate.toLocaleDateString().replace(/\//g, '-');
      this.queryMeetingForUser();
      this.queryAllMeetings();
      this.queryAllRoom();
      this.drawMeetingRoom();
      this.drawRoom();
	  this.querymyChartoption();
	  this.querymyRoomChartoption();
	  this.setChartOption();
    }
  }
</script>

<style scoped>
  .time {
    font-size: 17px;
    font-weight: bold;
    color: purple;
  }

  .content {
    font-size: 14px;
    padding-left: 5px;
    color: dimgrey;
    font-weight: bold;
  }

  .meeting {
    background-color: #967adc;
  }

  .meetingRoom {
    background-color: #70ca63;
  }

  .bookedMeeting {
    background-color: #e9573f;
  }

  .todayMeeting {
    background-color: #3bafda;
  }

  h2 {
    padding: 5px;
    position: relative;
    color: #f5f2fd;
    font-size: 24px;
    line-height: 15px;
    margin-top: 19px;
  }

  h5 {
    padding: 5px;
    position: relative;
    color: #f5f2fd;
    font-size: 17px;
  }

  i {
    position: absolute;
    opacity: 0.8;
    right: 0;
    top: 10px;
    line-height: 100px;
    font-size: 80px;
  }
</style>
