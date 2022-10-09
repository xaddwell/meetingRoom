from django.db import models
from backend.users.models import User

# Create your models here.




class MeetingRoom(models.Model):
    statusChoice = (
        (0, '可使用'),
        (1, '不可使用'),
    )
    roomId = models.CharField("会议室编号", max_length=10,default=0)
    roomName = models.CharField('会议室名称', max_length=10,default=0)
    capacity = models.IntegerField('会议室容量', default=0)
    air_conditioner = models.IntegerField('空调', choices=statusChoice, default=0)
    projector = models.IntegerField('投影仪', choices=statusChoice, default=0)
    img = models.ImageField('会议室预览图', upload_to='meetingRoom/', default='/meetingRoom/default.jpeg')

    def __str__(self):
        return 'roomId %s'%(self.roomId)

    class Meta:
        db_table = 'MeetingRoom'


class MeetingRoomStatus(models.Model):
    statusChoice = (
        (0, '故障'),
        (1, '9'),
        (2, '11'),
        (3, '13'),
        (4, '15'),
        (5, '17')
    )
    date=models.DateField('时间',auto_created=True)
    status = models.IntegerField('会议室状态', choices=statusChoice, default=0)
    belong = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)

    def __str__(self):
        return 'roomstatus %s'%(self.status)

    class Meta:
        db_table = 'MeetingRoomStatus'


class Device(models.Model):
    statusChoice = (
        (0, '可使用'),
        (1, '维修中')
    )
    deviceName = models.CharField('设备名称', max_length=15)
    num = models.IntegerField('设备数量')
    status = models.IntegerField('设备状态', choices=statusChoice, default=0)
    belong = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Device'


class Meeting(models.Model):
    statusChoice = (
        (0, '待审核'),
        (1, '待执行'),
        (2, '已取消'),
        (3, '已完成'),
        (4, '审核未通过')
    )
    import django.utils.timezone as timezone
    startTime = models.DateTimeField('开始时间')
    applyTime = models.DateTimeField('申请时间',default=timezone.now())
    departN = models.CharField('申请部门', max_length=20, default="")
    endTime = models.DateTimeField('结束时间')
    subject = models.CharField('会议主题', max_length=40,default="")
    meetingRoom = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    status = models.IntegerField('会议状态', choices=statusChoice, default=0)

    class Meta:
        db_table = 'Meeting'


class Participant(models.Model):
    statusChoice = (
        (0, '未签到'),
        (1, '已签到')
    )
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField('签到状态', choices=statusChoice, default=0)

    class Meta:
        db_table = 'Participant'


class Log(models.Model):
    person = models.CharField('用户名称', max_length=30)
    action = models.CharField('操作行为', max_length=100)
    time = models.DateTimeField('操作时间', auto_now=True)

    def __str__(self):
        return self.action

    class Meta:
        db_table = 'Log'
