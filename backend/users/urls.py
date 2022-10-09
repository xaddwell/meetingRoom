from django.contrib import admin
from django.urls import path
from backend.users import views

urlpatterns = [
    path('getUserList', views.getUserList),
    path('login', views.login),
    path('register', views.register),
    path('changePassword', views.changePassword),
    path('resetPassword', views.resetPassword),
    path('searchUser', views.searchUser),
    path('editUser', views.editUser),
    path('deleteUser', views.deleteUser),
    path('uploadImg', views.uploadImg),
    path('addDepartment', views.addDepartment),
    path('getDeptList', views.getDeptList),
    path('deleteDepartment', views.deleteDepartment),
    path('searchDept', views.searchDept),
    path('editDept', views.editDept),
    path('changeUserDept', views.changeUserDept)
]
