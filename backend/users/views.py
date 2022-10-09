from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db.models import Q
import hashlib
import os
from MeetingRoom.settings import BASE_DIR

from backend.users.models import User, Department
from backend.meeting.models import Log

uType = {
        '普通用户': 0,
        '管理员': 1
    }


def generateLog(person, content):
    newlog = Log()
    newlog.person = person
    newlog.action = content
    newlog.save()
    # print(newlog)


@require_http_methods('GET')
def getUserList(request: HttpRequest):
    # print(request.GET)
    currentPage = int(request.GET['currentPage'])
    pageSize = int(request.GET['pageSize'])
    distributed = request.GET['distribute']
    way = request.GET['way']
    response = {'users': []}
    if way == 'all':
        users = User.objects.all()
    elif way == 'dept':
        if distributed == 'no':
            users = User.objects.filter(department=None)
        else:
            dept = request.GET['dept']
            dept = Department.objects.get(departmentId=dept)
            users = User.objects.filter(department=dept.id)
            # print(users)
    total = len(users)
    response['total'] = total
    pages = total // pageSize

    if currentPage > pages:  # 请求数据不够显示一页
        users = users[(currentPage-1)*pageSize:]
    else:  # 请求数据够显示一页
        users = users[(currentPage-1)*pageSize: currentPage*pageSize]

    for usr in users:
        temp = {'id': usr.id, 'username': usr.username, 'phone': usr.phone, 'email': usr.email,
                'usrType': usr.get_userType_display(), 'img': 'http://127.0.0.1:8000/media/' + usr.img.name,
                'dept': usr.department.departmentId if usr.department else '未分配部门'}
        response['users'].append(temp)
    response['num'] = len(users)
    return JsonResponse(response)


@require_http_methods('POST')
def login(request: HttpRequest):
    response = {}
    # print(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    isadmin = request.POST['isadmin']

    # print(isadmin == 'true')
    user = User.objects.filter(username=username)
    if not user:
        response['status'] = 1
        response['msg'] = '用户名不存在'
        return JsonResponse(response)

    obj_hash = hashlib.md5()
    obj_hash.update(password.encode())
    password = obj_hash.hexdigest()

    if password != user[0].password:
        response['status'] = 2
        response['msg'] = '密码错误'
        return JsonResponse(response)

    if isadmin == 'true' and user[0].userType != 1:
        response['status'] = 3
        response['msg'] = '用户权限不够'
        return JsonResponse(response)

    response['status'] = 0
    response['userType'] = user[0].userType
    response['msg'] = '登陆成功'
    return JsonResponse(response)


@require_http_methods('POST')
def register(request: HttpRequest):
    username = request.POST['username']
    password = request.POST['password']
    phone = request.POST['phone']
    response = {}
    user = User.objects.filter(username=username)
    if user:
        response['msg'] = '该用户名已存在'
        response['status'] = 1
        return JsonResponse(response)
    user = User(username=username, phone=phone)
    obj_hash = hashlib.md5()
    obj_hash.update(password.encode())
    password = obj_hash.hexdigest()
    user.password = password
    if 'email' in request.POST:
        user.email = request.POST['email']
    user.save()
    response['msg'] = '注册成功'
    response['status'] = 0
    return JsonResponse(response)


@require_http_methods('POST')
def changePassword(request: HttpRequest):
    # print(request.POST)
    response = {}
    username = request.POST['username']
    newpassword = request.POST['newpassword']
    oldpassword = request.POST['oldpassword']
    user = User.objects.filter(username=username)[0]
    obj_hash = hashlib.md5()
    obj_hash.update(oldpassword.encode())
    oddpassword = obj_hash.hexdigest()
    if oddpassword != user.password:
        response['msg'] = '密码错误'
        response['status'] = 1
    else:
        obj_hash = hashlib.md5()
        obj_hash.update(newpassword.encode())
        newpassword = obj_hash.hexdigest()
        user.password = newpassword
        user.save()
        response['msg'] = '密码修改成功'
        response['status'] = 0
    return JsonResponse(response)


@require_http_methods('POST')
def resetPassword(request: HttpRequest):
    # print(request.POST)
    username = request.POST['username']
    usr = request.POST['usr']
    response = {}
    try:
        user = User.objects.filter(username=usr)[0]
        obj_hash = hashlib.md5()
        obj_hash.update("1234567890".encode())
        password = obj_hash.hexdigest()
        user.password = password
        user.save()
        content = '{}重置了用户{}的密码'.format(username, usr)
        generateLog(username, content)
        response['msg'] = '重置密码成功'
        response['status'] = 0
    except:
        response['msg'] = '重置密码异常'
        response['status'] = 1
    #     print('重置密码异常')
    return JsonResponse(response)


def searchUser(request: HttpRequest):
    # print(request.GET)
    way = request.GET['way']
    keyword = request.GET['keyword']
    response = {'users': []}
    if way == 'username':
        users = User.objects.filter(username=keyword)
        if not users:
            response['msg'] = '请输入有效用户名'
            response['status'] = 1
            return JsonResponse(response)
    elif way == 'usrType':
        usrType = uType[keyword]
        users = User.objects.filter(userType=usrType)
    elif way == 'dept':
        dept = Department.objects.get(departmentId=keyword)
        users = User.objects.filter(department=dept)

    response['total'] = len(users)
    for user in users:
        temp = {'id': user.id, 'username': user.username, 'phone': user.phone, 'email': user.email,
                'usrType': user.get_userType_display(), 'img': 'http://127.0.0.1:8000/media/' + user.img.name,
                'dept': user.department.departmentId if user.department else '未分配部门'}
        temp['deptName'] = user.department.departmentName if user.department else '未分配部门'
        response['users'].append(temp)
    response['msg'] = '查询成功'
    response['status'] = 0
    return JsonResponse(response)


def editUser(request: HttpRequest):
    print(request.GET)
    response = {}
    usr = request.GET['usr']
    phone = request.GET['phone']
    email = request.GET['email']
    usrType = request.GET['usrType']
    username = request.GET['username']
    usrType = uType[usrType]
    try:
        user = User.objects.filter(username=usr)[0]
        user.phone = phone
        user.email = email
        user.userType = usrType
        user.save()
        if not 'manage' in request.GET:
            content = '{}修改了用户{}的信息'.format(username, usr)
            generateLog(username, content)
        response['msg'] = '修改用户信息成功'
        response['status'] = 0
    #     # print(2)
    except:
    #     # print(1)
        response['msg'] = '修改用户信息失败'
        response['status'] = 1
    return JsonResponse(response)


def deleteUser(request: HttpRequest):
    print(request.GET)
    usr = request.GET['usr']
    username = request.GET['username']
    response = {}
    try:
        user = User.objects.filter(username=usr)
        user.delete()
        content = '{}删除了用户{}的信息'.format(username, usr)
        generateLog(username, content)
        response['msg'] = '删除成功'
        response['status'] = 0
    except:
        response['msg'] = '删除失败'
        response['status'] = 1
    return JsonResponse(response)


def uploadImg(request: HttpRequest):
    print(request.POST)
    print(request.FILES)
    file = request.FILES.get('file', None)  # 获取上传文件
    username = request.POST['username']  # 获取用户名
    file.name = username + '.' + file.name.split('.')[1]
    # 判断是否存在当前用户的头像，每位用户只留一张头像
    user = User.objects.get(username=username)
    head_path = os.path.join(BASE_DIR, 'media\\')
    if os.path.exists(os.path.join(head_path, user.img.name)) and user.img.name != 'user_img/default.jpeg':
        os.remove(os.path.join(head_path, user.img.name))
    user.img = file
    user.save()
    return JsonResponse({})

# file_path = head_path + file.name
# with open(file_path, 'wb') as f:
#     for chunk in file.chunks():
#         f.write(chunk)
#         f.flush()
# user = User.objects.get(username='test')
# print(user.img.name)
# user.img = file
# print(user.img)


def changeUserDept(request: HttpRequest):
    response = {}
    # print(request.GET)
    usr = request.GET['usr']
    dept = request.GET['dept']
    username = request.GET['username']
    user = User.objects.get(username=usr)
    dept = Department.objects.get(departmentId=dept)
    user.department = dept
    user.save()
    content = '{}更改了用户{}的部门'.format(username,user.username)
    # print(content)
    generateLog(username, content)
    response['msg'] = '部门更改成功'
    response['status'] = 0
    return JsonResponse(response)

# ===============================下面是关于部门的处理======================================


def addDepartment(request: HttpRequest):
    print(request.POST)
    response = {}
    deptId = request.POST['deptNo']
    deptName = request.POST['deptName']
    deptPhone = request.POST['deptPhone']
    username = request.POST['username']
    dept = Department.objects.filter(departmentId=deptId)
    if dept:
        response['msg'] = '该部门已存在'
        response['status'] = 1
        return JsonResponse(response)

    dept = Department()
    dept.departmentId = deptId
    dept.departmentName = deptName
    dept.phone = deptPhone
    dept.save()
    content = '{}添加了部门{}'.format(username, deptId)
    generateLog(username, content)
    response['msg'] = '添加部门成功'
    response['status'] = 0
    return JsonResponse(response)


def getDeptList(request: HttpRequest):
    # print(request)
    # print(request.GET)
    response = {}
    response['depts'] = []
    depts = list(Department.objects.all())
    depts.sort(key=lambda x: x.departmentId)  # 按部门id升序排序
    if 'all' in request.GET:
        for dept in depts:
            dic = {'deptNo': dept.departmentId, 'deptName': dept.departmentName, 'deptPhone': dept.phone}
            response['depts'].append(dic)
        return JsonResponse(response)

    currentPage = int(request.GET['currentPage'])
    pageSize = int(request.GET['pageSize'])
    # print(depts)
    total = len(depts)
    response['total'] = total
    pages = total // pageSize
    if currentPage > pages:  # 请求数据不够显示一页
        depts = depts[(currentPage-1)*pageSize:]
    else:  # 请求数据够显示一页
        depts = depts[(currentPage-1)*pageSize: currentPage*pageSize]

    for dept in depts:
        dic = {}
        dic['deptNo'] = dept.departmentId
        dic['deptName'] = dept.departmentName
        dic['deptPhone'] = dept.phone
        response['depts'].append(dic)
    return JsonResponse(response)


def deleteDepartment(request: HttpRequest):
    response = {}
    deptId = request.GET['deptId']
    username = request.GET['username']
    try:
        dept = Department.objects.filter(departmentId=deptId)[0]
        dept.delete()
        content = '{}删除了部门{}'.format(username, deptId)
        generateLog(username, content)
        response['msg'] = '删除部门成功'
        response['status'] = 0
    except:
        response['msg'] = '删除部门失败'
        response['status'] = 1
    return JsonResponse(response)


def searchDept(request: HttpRequest):
    response = {}
    response['depts'] = []
    keyword = request.GET['keyword']
    way = request.GET['way']
    # print(way)
    if way == 'deptNo':
        depts = Department.objects.filter(departmentId=keyword)
        if not depts:
            response['msg'] = '请输入有效部门编号'
            response['status'] = 1
            return JsonResponse(response)
    elif way == 'deptName':
        depts = Department.objects.filter(departmentName=keyword)

    depts = list(depts)
    depts.sort(key=lambda x: x.departmentId)  # 按部门id升序排序
    response['total'] = len(depts)
    for dept in depts:
        dic = {}
        dic['deptNo'] = dept.departmentId
        dic['deptName'] = dept.departmentName
        dic['deptPhone'] = dept.phone
        response['depts'].append(dic)
        response['status'] = 0
        response['msg'] = '查询部门成功！'
    return JsonResponse(response)


def editDept(request: HttpRequest):
    print(request.GET)
    response = {}
    username = request.GET['username']
    try:
        dept = Department.objects.filter(departmentId=request.GET['deptNo'])[0]
        dept.departmentName = request.GET['deptName']
        dept.phone = request.GET['deptPhone']
        dept.save()
        content = '{}修改了部门{}的信息'.format(username, request.GET['deptNo'])
        generateLog(username, content)
        response['msg'] = '修改部门信息成功'
        response['status'] = 0
    except:
        response['msg'] = '修改部门信息失败'
        response['status'] = 1
    return JsonResponse(response)
