from django.db import models
from Boss.models import Job

# Create your models here.

# 管理员表
class Admins(models.Model):
	email = models.EmailField(verbose_name='邮箱',default=0)
	password = models.CharField(max_length=32, verbose_name='密码')
	name = models.CharField(max_length=32, null=True, blank=True, verbose_name='用户名')
	phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
	## type 中
		## 0 代表求职者
		## 1 代表企业
		## 2 代表管理员
	type = models.CharField(max_length=4,null=True, blank=True, verbose_name='类别')
	photo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='头像')
	age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
	gender = models.CharField(max_length=4, null=True, blank=True, verbose_name='性别')
	address = models.TextField(null=True, blank=True, verbose_name='地址')

	class Meta:
		db_table = 'admins'

# 企业发布的职位审核状态表
# 职位状态


# class Check(models.Model):
# 	# 职位名称，公司，发布人，时间，状态
# 	j_name = models.ForeignKey(to=Job,on_delete=models.CASCADE)
#
#
# 	class Meta:
# 		db_table = 'check'