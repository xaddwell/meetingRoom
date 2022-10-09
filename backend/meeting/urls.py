from django.contrib import admin
from django.urls import path
from backend.meeting import views

urlpatterns = [
    # path('/getUserList', views.getUserList),
    path('addMeetingRoom', views.addMeetingRoom),
    path('getRoomList', views.getRoomList),
    path('deleteRoom', views.deleteRoom),
    path('searchRoom', views.searchRoom),
    path('uploadRoomImg', views.uploadRoomImg),
    path('editRoom', views.editRoom),
    path('getLogList', views.getLogList),
    path('searchLog', views.searchLog),
    path('logexport', views.logexport),
    path('devicechange', views.devicechange),

    path('selectRoom', views.selectRoom),
    path('getManagerRoomList', views.getManagerRoomList),

    path('QueryAllRoom', views.QueryAllRoom),
    path('QuerymyRoomChartoption', views.QuerymyRoomChartoption),
    path('QuerymyChartoption', views.QuerymyChartoption),
    path('selectDept', views.selectDept),

    path('getAcceptList', views.getAcceptList),
    path('getRejectList', views.getRejectList),
    path('meetingReject', views.meetingReject),
    path('meetingAccept', views.meetingAccept),

    path('QueryMeetingForUser', views.QueryMeetingForUser),
    path('QueryAllMeetings', views.QueryAllMeetings),

    path('getBookableRoomList', views.getBookableRoomList),
    path('meetingSubmit', views.meetingSubmit),
    path('deleteMeeting', views.deleteMeeting),
    path('getMeetingList', views.getMeetingList),

    path('getManagerApprovedMeetingList', views.getManagerApprovedMeetingList),
    path('getManagerNotApprovedMeetingList', views.getManagerNotApprovedMeetingList),
    path('getApprovedMeetingList', views.getApprovedMeetingList),
    path('getNotApprovedMeetingList', views.getNotApprovedMeetingList),
    path('getApprovingMeetingList', views.getApprovingMeetingList),
    path('getDoneList', views.getDoneList),
    path('getNotDoneList', views.getNotDoneList),

    path('CameraSignIn', views.CameraSignIn),
]
