from django.db import models

# Create your models here.


class Department(models.Model):
    departmentId = models.CharField('部门编号', max_length=10)
    departmentName = models.CharField("部门名称", max_length=20)
    phone = models.CharField('联系方式', max_length=11)

    def __str__(self):
        return 'Department %s'%(self.departmentName)

    class Meta:
        db_table = 'Department'


class User(models.Model):
    userTypeChoice = (
        (0, '普通用户'),
        (1, '管理员')
    )
    username = models.CharField("用户名", max_length=30, unique=True)
    password = models.CharField("密码", max_length=32)
    phone = models.CharField("电话号码", max_length=11)
    email = models.CharField("邮箱", max_length=30)
    userType = models.IntegerField("用户类型", choices= userTypeChoice, default=0)
    department = models.ForeignKey(Department, models.SET_NULL, blank=True, null=True,)
    img = models.ImageField('用户头像', upload_to='user_img/', default='user_img/default.jpeg')

    def __str__(self):
        return 'username %s'%(self.username)

    class Meta:
        db_table = 'User'

