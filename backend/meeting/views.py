from django.shortcuts import render
# Create your views here.
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse, HttpRequest
import os
from backend.meeting.models import Participant, Meeting, MeetingRoom, Log, MeetingRoomStatus
from MeetingRoom.settings import BASE_DIR
from backend.users.views import generateLog
from backend.users.models import User, Department
import csv
from copy import copy
import datetime

timeMap = {"09:00": 1, "10:30": 2, "13:00": 3, "15:00": 4, "17:00": 5}


# ====================================下面是会议室管理部分===============================


def addMeetingRoom(request: HttpRequest):
    # print(request.POST)
    response = {}
    roomNo = request.POST['roomNo']
    roomName = request.POST['roomName']
    roomSize = request.POST['roomSize']
    username = request.POST['username']

    room = MeetingRoom.objects.filter(roomId=roomNo)
    if room:
        response['msg'] = '该会议室已存在'
        response['status'] = 1
        return JsonResponse(response)

    room = MeetingRoom()
    room.roomId = roomNo
    room.roomName = roomName
    room.capacity = roomSize
    room.save()
    content = '{}添加了会议室{}'.format(username, roomNo)
    generateLog(username, content)
    response['msg'] = '添加会议室成功'
    response['status'] = 0
    return JsonResponse(response)


def getRoomList(request: HttpRequest):
    currentPage = int(request.GET['currentPage'])
    pageSize = int(request.GET['pageSize'])
    response = {'rooms': []}
    rooms = list(MeetingRoom.objects.all())
    rooms.sort(key=lambda x: x.roomId)  # 按会议室id升序排序
    # print(rooms)
    total = len(rooms)
    response['total'] = total
    pages = total // pageSize
    # print(pages)
    if currentPage > pages:  # 请求数据不够显示一页
        rooms = rooms[(currentPage - 1) * pageSize:]
    else:  # 请求数据够显示一页
        rooms = rooms[(currentPage - 1) * pageSize: currentPage * pageSize]

    for room in rooms:
        dic = {'roomNo': room.roomId, 'roomName': room.roomName, 'roomSize': room.capacity,
               'img': 'http://127.0.0.1:8000/media' + room.img.name, 'air': room.air_conditioner == 0,
               'projector': room.projector == 0}
        # print(room)
        # print(dic)
        ms = MeetingRoomStatus.objects.filter(belong=room)
        if not ms:
            dic['roomStatus'] = '空闲中'
        else:
            dic['roomStatus'] = '占用中'
        response['rooms'].append(dic)
    return JsonResponse(response)


def searchRoom(request: HttpRequest):
    # print(request)
    response = {'rooms': []}
    keyword = request.GET['keyword']
    way = request.GET['way']
    if way == 'roomId':
        rooms = MeetingRoom.objects.filter(roomId=keyword)
        if not rooms:
            response['msg'] = '请输入有效会议室号'
            response['status'] = 1
    elif way == 'status':
        dic = {
            '空闲中': 0, '已预约': 1, '维修中': 2
        }
        status = dic[keyword]
        rooms = MeetingRoom.objects.filter(status=status)
    elif way == 'all':
        rooms = list(MeetingRoom.objects.all())

    response['total'] = len(rooms)
    rooms = list(rooms)
    rooms.sort(key=lambda x: x.roomId)  # 按会议室id升序排序
    for room in rooms:
        # print(room)
        dic = {'roomNo': room.roomId, 'roomName': room.roomName, \
               'roomSize': room.capacity, 'img': 'http://127.0.0.1:8000/media' + room.img.name}
        ms = MeetingRoomStatus.objects.filter(belong=room)
        if not ms:
            dic['roomStatus'] = '空闲中'
        else:
            dic['roomStatus'] = '占用中'
        response['rooms'].append(dic)
    return JsonResponse(response)


def deleteRoom(request: HttpRequest):
    response = {}
    # print(request.GET)
    roomId = request.GET['roomId']
    username = request.GET['username']
    try:
        room = MeetingRoom.objects.filter(roomId=roomId)[0]
        room.delete()
        content = '{}删除了会议室{}'.format(username, roomId)
        generateLog(username, content)
        response['msg'] = '删除会议室成功'
        response['status'] = 0
    except:
        response['msg'] = '删除会议室失败'
        response['status'] = 1
    return JsonResponse(response)


def uploadRoomImg(request: HttpRequest):
    print(request.POST)
    print(request.FILES)
    file = request.FILES.get('file', None)  # 获取上传文件
    roomId = request.POST['roomNo']  # 获取会议室ID
    file.name = roomId + '.' + file.name.split('.')[1]
    # 判断是否存在当前用户的头像，每位用户只留一张头像
    room = MeetingRoom.objects.get(roomId=roomId)
    head_path = os.path.join(BASE_DIR, 'media\\')
    if os.path.exists(os.path.join(head_path, room.img.name)) and room.img.name != 'user_img/default.jpeg':
        os.remove(os.path.join(head_path, room.img.name))
    room.img = file
    room.save()
    return JsonResponse({})


def editRoom(request: HttpRequest):
    # print(request.GET)
    response = {}
    roomId = request.GET['roomNo']
    roomName = request.GET['roomName']
    roomSize = request.GET['roomSize']
    username = request.GET['username']
    try:
        room = MeetingRoom.objects.filter(roomId=roomId)[0]
        room.roomName = roomName
        room.capacity = roomSize
        room.save()
        content = '{}修改了会议室{}的信息'.format(username, roomId)
        generateLog(username, content)
        response['msg'] = '修改会议室成功'
        response['status'] = 0
        # print(2)
    except:
        # print(1)
        response['msg'] = '修改会议室失败'
        response['status'] = 1

    return JsonResponse(response)

def selectRoom(request: HttpRequest):

    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'meetingSize': 0, 'meetingDate': '', 'deptName': '',
                        'roomNo': 0,'meetingTheme': '','meetingSlot':''}
            room=MeetingRoom.objects.filter(roomId=request.GET['roomId'])[0]
            meetings = Meeting.objects.filter(meetingRoom_id=room.id)
            meetingIdList = []
            for meeting in meetings:
                if  (meeting.status !=3 and request.GET['pass']=='0') or \
                        (meeting.status==3 and request.GET['pass']=='1'):
                    temp = copy(template)
                    temp['meetingSize'] = meeting.meetingRoom.capacity
                    temp['meetingDate'] = str(meeting.applyTime)[:10]
                    temp['meetingSlot'] = timeMap[str(meeting.startTime).split(' ')[1][:5]]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])

            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {}
            response['code'] = 100
            response['extend'] = {}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]
            print(response)

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {}
            response['code'] = 100
            response['error'] = e
            return JsonResponse(response)

def getManagerRoomList(request: HttpRequest):
    response = {}
    response['extend'] = {}
    response['extend']['result']=[]
    rooms = list(MeetingRoom.objects.all())
    rooms.sort(key=lambda x: x.roomId)  # 按部门id升序排序

    currentPage = int(request.GET['currentPage'])
    pageSize = int(request.GET['pageSize'])
    # print(depts)
    total = len(rooms)
    response['total'] = total
    pages = total // pageSize
    if currentPage > pages:  # 请求数据不够显示一页
        rooms = rooms[(currentPage - 1) * pageSize:]
    else:  # 请求数据够显示一页
        rooms = rooms[(currentPage - 1) * pageSize: currentPage * pageSize]

    for room in rooms:
        dic = {}
        dic['roomId'] = room.roomId
        dic['roomName'] = room.roomName
        response['extend']['result'].append(dic)
    response['code']=100

    return JsonResponse(response)


def devicechange(request: HttpRequest):
    print(request.GET)
    response = {}
    username = request.GET['username']
    roomId = request.GET['roomId']
    info = request.GET['info']
    device = request.GET['device']
    status = 0 if info == 'true' else 1
    try:
        room = MeetingRoom.objects.get(roomId=roomId)
        if device == 'projector':
            room.projector = status
        elif device == 'air':
            room.air_conditioner = status
        room.save()
        content = '{}修改了会议室{} {}的状态'.format(username, roomId, device)
        generateLog(username, content)
        response['status'] = 0
        response['msg'] = '设备状态修改成功'
    except:
        response['status'] = 1
        response['msg'] = '设备状态修改失败'
    return JsonResponse(response)


# ===================================下面是会议管理部分======================================================


def QueryAllRoom(request: HttpRequest):
    template = {'meetingRoomName': ''}
    if request.method == 'GET':
        user = User.objects.filter(username=request.GET['username'])[0]
        rooms = MeetingRoom.objects.all()
        roomList = []
        for p in rooms:
            temp = copy(template)
            temp['meetingRoomName'] = p.roomName
            roomList.append(temp)
        response = roomList
        return JsonResponse(response, safe=False)


def QuerymyRoomChartoption(request: HttpRequest):
    response = {'series': [{'data': [10, 2, 10, 11, 50, 5, 8]}], }
    return JsonResponse(response)


def QuerymyChartoption(request: HttpRequest):
    if request.method == 'GET':
        try:
            response = {'series': [{'data': ''}], }
            user = User.objects.filter(username=request.GET['username'])[0]
            partition = Participant.objects.filter(person_id=user.id)
            roomList = {}
            for p in partition:
                meeting = Meeting.objects.filter(id=p.meeting_id)[0]
                name = meeting.meetingRoom.roomName
                if name not in roomList:
                    roomList[name] = 1
                else:
                    roomList[name] += 1

            returnList = []
            for k, v in roomList.items():
                temp = {'value': v, 'name': k}
                returnList.append(temp)

            response['series'][0]['data'] = returnList
            print(response)
            return JsonResponse(response, safe=False)

        except Exception as e:
            response = {'code': 500, 'error': e}
            return JsonResponse(response)


def selectDept(request: HttpRequest):

    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'meetingSize': 0, 'meetingDate': '', 'deptName': '',
                        'roomNo': 0,'meetingTheme': '','meetingSlot':''}
            department=Department.objects.filter(id=request.GET['deptId'])[0]
            meetings = Meeting.objects.filter(departN=department.departmentName)
            meetingIdList = []
            for meeting in meetings:
                if  (meeting.status != 3 and request.GET['pass']=='0') or \
                        (meeting.status==3 and request.GET['pass']=='1'):
                    temp = copy(template)
                    temp['meetingSize'] = meeting.meetingRoom.capacity
                    temp['meetingDate'] = str(meeting.applyTime)[:10]
                    temp['meetingSlot'] = timeMap[str(meeting.startTime).split(' ')[1][:5]]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])

            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {}
            response['code'] = 100
            response['extend'] = {}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]
            print(response)

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {}
            response['code'] = 100
            response['error'] = e
            return JsonResponse(response)


def QueryMeetingForUser(request: HttpRequest):
    template = {'meetingDate': '', 'meetingTopic': '', 'meetingRoomName': '', 'meetingStartTime': '',
                'meetingEndTime': ''}
    if request.method == 'GET':
        user = User.objects.filter(username=request.GET['username'])[0]
        partition = Participant.objects.filter(person_id=user.id)
        meetingIdList = []
        for p in partition:
            meeting = Meeting.objects.filter(id=p.meeting_id)[0]
            meetingStatus = MeetingRoomStatus.objects.filter(belong_id=p.meeting.meetingRoom.id)[0]
            temp = copy(template)
            temp['meetingStartTime'] = str(meeting.startTime)[10:16]
            temp['meetingEndTime'] = str(meeting.endTime)[10:16]
            temp['meetingDate'] = meetingStatus.date
            temp['meetingRoomName'] = meeting.meetingRoom.roomName
            temp['meetingTopic'] = meeting.subject
            meetingIdList.append(temp)

        response = meetingIdList
        return JsonResponse(response, safe=False)


def QueryAllMeetings(request: HttpRequest):
    template = {'meetingDate': '', 'meetingTopic': '', 'meetingRoomName': '', 'meetingStartTime': '',
                'meetingEndTime': ''}
    if request.method == 'GET':
        user = User.objects.filter(username=request.GET['username'])[0]
        partition = Participant.objects.filter(person_id=user.id)
        meetingIdList = []
        for p in partition:
            meeting = Meeting.objects.filter(id=p.meeting_id)[0]
            meetingStatus = MeetingRoomStatus.objects.filter(belong_id=p.meeting.meetingRoom.id)[0]
            temp = copy(template)
            temp['meetingStartTime'] = str(meeting.startTime)[10:16]
            temp['meetingEndTime'] = str(meeting.endTime)[10:16]
            temp['meetingDate'] = meetingStatus.date
            temp['meetingRoomName'] = meeting.meetingRoom.roomName
            temp['meetingTopic'] = meeting.subject
            meetingIdList.append(temp)

        response = meetingIdList
        return JsonResponse(response, safe=False)


def getBookableRoomList(request: HttpRequest):
    if request.method == 'GET':
        pageSize = int(request.GET['pageSize'])
        currentPage = int(request.GET['currentPage'])
        applyDate = request.GET['applyDate']
        template = {'roomId': 1, 'roomNo': 312, 'roomSize': 10, 'air': True, 'projector': True,
                    'one': True, 'two': True, 'three': True, 'four': True, 'five': True}

        rooms = MeetingRoom.objects.all()
        roomstatus = MeetingRoomStatus.objects.filter(date=applyDate)

        statusList = {}
        for status in roomstatus:
            name = str(status.belong.roomName)
            if name not in statusList:
                statusList[name] = [str(status.status)]
            else:
                statusList[name].append(str(status.status))

        roomList = []
        for index, room in enumerate(rooms):
            temp = copy(template)
            name = str(room.roomName)
            temp['roomId'] = index
            temp['roomNo'] = name
            temp['roomSize'] = room.capacity
            temp['air'] = not (room.air_conditioner)
            temp['projector'] = not room.projector
            if name in statusList:
                for k in statusList[name]:
                    if k == '0':
                        temp['one'] = False
                        temp['two'] = False
                        temp['three'] = False
                        temp['four'] = False
                        temp['five'] = False

                    elif k == '1':
                        temp['one'] = False
                    elif k == '2':
                        temp['two'] = False
                    elif k == '3':
                        temp['three'] = False
                    elif k == '4':
                        temp['four'] = False
                    elif k == '5':
                        temp['five'] = False
            roomList.append(temp)

        response = {'code': 100, 'extend': {}}
        response['extend']['result'] = {}
        response['extend']['result']['total'] = len(roomList)
        start = (currentPage - 1) * pageSize
        end = min(currentPage * pageSize, len(roomList) - (currentPage - 1) * pageSize)
        response['extend']['result']['list'] = roomList[start:end]

        return JsonResponse(response)


def meetingSubmit(request: HttpRequest):
    if request.method == 'PUT':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            room = MeetingRoom.objects.filter(roomName=request.GET['roomNo'])[0]
            department = Department.objects.filter(id=user.department_id)[0]
            meeting = Meeting()
            roomstatus = MeetingRoomStatus()
            participants = Participant()

            meeting.subject = request.GET['meetingTheme']
            meeting.departN = department.departmentName
            meeting.meetingRoom = room

            str2time = datetime.datetime.strptime
            applyDate = request.GET['applyDate']
            displaySlot = request.GET['displaySlot']
            applySlot = request.GET['applySlot']
            startTime = displaySlot.split('-')[0]
            endTime = displaySlot.split('-')[1]
            startTime = str2time(applyDate + " " + startTime, '%Y-%m-%d %H:%M')
            endTime = str2time(applyDate + " " + endTime, '%Y-%m-%d %H:%M')
            meeting.startTime = startTime
            meeting.endTime = endTime

            roomstatus.status = applySlot
            roomstatus.belong = room
            roomstatus.date = applyDate

            participants.person = user
            participants.meeting = meeting
            content = user.username + "添加会议_" + request.GET['roomNo'] + "_{}:{}".format(applyDate, displaySlot)
            generateLog(user.username, content)
            meeting.save()
            roomstatus.save()
            participants.save()

            response = {'code': 100}

        except Exception as e:

            print(e)
            response['code'] = 500
            response['error'] = e

        return JsonResponse(response)


def deleteMeeting(request: HttpRequest):
    if request.method == 'GET':
        DelMeetingId = int(request.GET['applicationId'])
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            meeting = Meeting.objects.filter(id=DelMeetingId)[0]
            meetingStatus = MeetingRoomStatus.objects.filter(belong_id=meeting.meetingRoom.id)[0]
            meetingStatus.delete()
            meeting.delete()

            content = '{}取消了会议预约'.format(user.username)
            generateLog(user.username, content)

            response = {'code': 100}
            return JsonResponse(response)

        except Exception as e:
            response = {'code': 500, 'error': e}
            return JsonResponse(response)


def getMeetingList(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'applicationId': 0, 'applyDate': '', 'applyTime': '', 'deptName': '',
                        'roomNo': 0, 'meetingTheme': ''}
            partition = Participant.objects.filter(person_id=user.id)
            meetingIdList = []
            for p in partition:
                meeting = Meeting.objects.filter(id=p.meeting_id)[0]
                if meeting.status in [0, 1]:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=p.meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['applicationId'] = meeting.id
                    temp['applySlot'] = meetingStatus.status
                    temp['applyDate'] = meetingStatus.date
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])

            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)

            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)

        except Exception as e:
            response = {'code': 500, 'error': e}
            return JsonResponse(response)


def getApprovedMeetingList(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'meetingSize': 0, 'applyDate': '', 'applyTime': '', 'deptName': '', 'roomNo': 0,
                        'meetingTheme': ''}
            partition = Participant.objects.filter(person_id=user.id)
            meetingIdList = []
            for p in partition:
                meeting = Meeting.objects.filter(id=p.meeting_id)[0]
                if meeting and meeting.status == 1:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=p.meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['applySlot'] = meetingStatus.status
                    temp['meetingSize'] = p.meeting.meetingRoom.capacity
                    temp['applyDate'] = meetingStatus.date
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])
            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getNotApprovedMeetingList(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'meetingSize': 0, 'applyDate': '', 'applyTime': '', 'deptName': '', 'roomNo': 0,
                        'meetingTheme': '', 'rejectReason': 'None'}
            partition = Participant.objects.filter(person_id=user.id)
            meetingIdList = []
            for p in partition:
                meeting = Meeting.objects.filter(id=p.meeting_id)[0]
                if meeting and meeting.status == 4:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['applySlot'] = timeMap[str(meeting.startTime).split(' ')[1][:5]]
                    temp['meetingSize'] = meeting.meetingRoom.capacity
                    temp['applyDate'] = meetingStatus.date
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])
            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getApprovingMeetingList(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'meetingSize': 0, 'applyDate': '', 'applyTime': '', 'deptName': '', 'roomNo': 0,
                        'meetingTheme': '', 'applySlot': 0}
            partition = Participant.objects.filter(person_id=user.id)
            meetingIdList = []
            for p in partition:
                meeting = Meeting.objects.filter(id=p.meeting_id)[0]
                if meeting and meeting.status == 0:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=p.meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['applySlot'] = meetingStatus.status
                    temp['meetingSize'] = p.meeting.meetingRoom.capacity
                    temp['applyDate'] = meetingStatus.date
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])

            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getNotDoneList(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'meetingSize': 0, 'meetingDate': '', 'deptName': '',
                        'roomNo': 0, 'meetingTheme': '', 'meetingSlot': ''}
            partition = Participant.objects.filter(person_id=user.id)
            meetingIdList = []
            for p in partition:
                meeting = Meeting.objects.filter(id=p.meeting_id)[0]
                if meeting and meeting.status in [0, 1, 2, 4]:
                    temp = copy(template)
                    temp['meetingSize'] = p.meeting.meetingRoom.capacity
                    temp['meetingDate'] = str(meeting.applyTime)[:10]
                    temp['meetingSlot'] = timeMap[str(meeting.startTime).split(' ')[1][:5]]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])

            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getDoneList(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            template = {'applySlot': 1, 'meetingSize': 0, 'meetingDate': '', 'deptName': '',
                        'roomNo': 0, 'meetingTheme': '', 'meetingSlot': ''}
            partition = Participant.objects.filter(person_id=user.id)
            meetingIdList = []
            for p in partition:
                meeting = Meeting.objects.filter(id=p.meeting_id)[0]
                if meeting and meeting.status == 3:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=p.meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['meetingSize'] = p.meeting.meetingRoom.capacity
                    temp['meetingDate'] = meetingStatus.date
                    temp['meetingSlot'] = timeMap[str(meeting.startTime).split(' ')[1][:5]]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])

            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getAcceptList(request: HttpRequest):
    if request.method == 'GET':
        try:
            template = {'applySlot': 1, 'meetingSize': 0, 'applyDate': '', 'applyTime': '', 'deptName': '', 'roomNo': 0,
                        'meetingTheme': ''}
            meetings = Meeting.objects.all()
            meetingIdList = []
            for meeting in meetings:
                if meeting.status in [1, 3]:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['applySlot'] = meetingStatus.status
                    temp['meetingSize'] = meeting.meetingRoom.capacity
                    temp['applyDate'] = meetingStatus.date
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])
            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getManagerApprovedMeetingList(request: HttpRequest):
    if request.method == 'GET':
        try:
            template = {'applySlot': 1, 'meetingSize': 0, 'applyDate': '', 'applyTime': '', 'deptName': '', 'roomNo': 0,
                        'meetingTheme': ''}
            meetings = Meeting.objects.all()
            meetingIdList = []
            for meeting in meetings:
                if meeting.status in [1, 3]:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['applySlot'] = meetingStatus.status
                    temp['meetingSize'] = meeting.meetingRoom.capacity
                    temp['applyDate'] = meetingStatus.date
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])
            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getManagerNotApprovedMeetingList(request: HttpRequest):
    if request.method == 'GET':
        try:
            template = {'applySlot': 1, 'meetingSize': 0, 'applyDate': '', 'applyTime': '', 'deptName': '', 'roomNo': 0,
                        'meetingTheme': '', 'applicationId': 0}
            meetings = Meeting.objects.all()
            meetingIdList = []
            for meeting in meetings:
                if meeting.status in [0]:
                    meetingStatus = MeetingRoomStatus.objects.filter(belong_id=meeting.meetingRoom.id)[0]
                    temp = copy(template)
                    temp['applySlot'] = meetingStatus.status
                    temp['applicationId'] = meeting.id
                    temp['meetingSize'] = meeting.meetingRoom.capacity
                    temp['applyDate'] = meetingStatus.date
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])
            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]

            print(response)

            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def getRejectList(request: HttpRequest):
    if request.method == 'GET':
        try:
            template = {'applySlot': 1, 'meetingSize': 0, 'applyDate': '', 'applyTime': '', 'deptName': '',
                        'roomNo': 0, 'meetingTheme': '', 'rejectReason': 'None'}
            meetings = Meeting.objects.all()
            meetingIdList = []
            for meeting in meetings:
                if meeting.status in [4]:
                    temp = copy(template)
                    temp['applySlot'] = timeMap[str(meeting.startTime).split(' ')[1][:5]]
                    temp['meetingSize'] = meeting.meetingRoom.capacity
                    temp['applyDate'] = str(meeting.applyTime)[:10]
                    temp['applyTime'] = str(meeting.applyTime)[:16]
                    temp['deptName'] = meeting.departN
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    temp['meetingTheme'] = meeting.subject
                    temp['roomNo'] = meeting.meetingRoom.roomName
                    meetingIdList.append(temp)

            pageSize = int(request.GET['pageSize'])
            currentPage = int(request.GET['currentPage'])
            start = (currentPage - 1) * pageSize
            end = min(currentPage * pageSize, len(meetingIdList) - (currentPage - 1) * pageSize)
            response = {'code': 100, 'extend': {}}
            response['extend']['result'] = {}
            response['extend']['result']['total'] = len(meetingIdList)
            response['extend']['result']['list'] = meetingIdList[start:end]
            return JsonResponse(response)
        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def meetingAccept(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            RejId = request.GET['applicationId']
            meetings = Meeting.objects.filter(id=RejId)[0]
            meetings.status = 1
            meetings.save()

            content = '{}同意了会议申请{}'.format(user.username, RejId)
            generateLog(user.username, content)

            response = {'code': 100}
            return JsonResponse(response)

        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


def meetingReject(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = User.objects.filter(username=request.GET['username'])[0]
            RejId = request.GET['applicationId']
            meetings = Meeting.objects.filter(id=RejId)[0]
            meetings.status = 4
            meetingStatus = MeetingRoomStatus.objects.filter(belong_id=meetings.meetingRoom.id)[0]
            meetingStatus.delete()
            meetings.save()
            content = '{}拒绝了会议{}'.format(user.username, RejId)
            generateLog(user.username, content)

            response = {'code': 100}
            return JsonResponse(response)

        except Exception as e:
            print(e)
            response = {'code': 100, 'error': e}
            return JsonResponse(response)


# ===================================下面是日志管理部分======================================================

def getLogList(request: HttpRequest):
    # print(request)
    # print(request.GET)
    currentPage = int(request.GET['currentPage'])
    pageSize = int(request.GET['pageSize'])
    response = {'logs': []}
    logs = (Log.objects.all())
    logs = logs[::-1]
    total = len(logs)
    response['total'] = total
    pages = total // pageSize
    # print(pages)
    if currentPage > pages:  # 请求数据不够显示一页
        logs = logs[(currentPage - 1) * pageSize:]
    else:  # 请求数据够显示一页
        logs = logs[(currentPage - 1) * pageSize: currentPage * pageSize]

    for log in logs:
        dic = {'person': log.person, 'action': log.action, 'time': log.time}
        response['logs'].append(dic)
    return JsonResponse(response)


def searchLog(request: HttpRequest):
    # print(request.GET)
    way = request.GET['way']
    keyword = request.GET['keyword']
    response = {'logs': []}
    if way == 'person':
        logs = Log.objects.filter(person=keyword)
        if not logs:
            response['msg'] = '请输入有效用户名'
            response['status'] = 1
            return JsonResponse(response)
    elif way == 'action':
        logs = Log.objects.filter(action__contains=keyword)

    response['total'] = len(logs)
    for log in logs:
        dic = {'person': log.person, 'action': log.action, 'time': log.time}
        response['logs'].append(dic)
    response['status'] = 0
    response['msg'] = '查询成功'
    return JsonResponse(response)


def logexport(request: HttpRequest):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="loginfo.csv"'
    logs = Log.objects.all()
    # print(logs)
    writer = csv.writer(response)
    writer.writerow(['操作人', '行为', '操作时间'])
    for log in logs:
        writer.writerow([log.person, log.action, log.time])
    return response


def CameraSignIn(request: HttpRequest):
    delId=int(request.GET['delete'])
    pp=Participant.objects.filter(person_id=delId)
    date=str(datetime.datetime.now())[:10]
    time=str(datetime.datetime.now())[11:16]
    for p in pp:
        meeting=Meeting.objects.filter(id=p.meeting_id)[0]

