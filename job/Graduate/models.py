from django.db import models
from Boss.models import Job_table


# Create your models here.

# 求职者用户表
class Hunter(models.Model):
	email = models.EmailField(verbose_name='邮箱', default=0)
	password = models.CharField(max_length=32, verbose_name='密码')
	name = models.CharField(null=True, blank=True, max_length=32, verbose_name='求职者名')
	phone = models.CharField(null=True, blank=True, max_length=11, verbose_name='手机号')
	## type 中
	## 0 代表求职者
	## 1 代表企业
	## 2 代表管理员
	type = models.CharField(max_length=4, verbose_name='类别')
	photo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='头像')
	age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
	gender = models.CharField(null=True, blank=True, max_length=4, verbose_name='性别')
	native = models.CharField(max_length=32, null=True, blank=True, verbose_name='籍贯')
	# 在线简历
	expect_job = models.CharField(null=True, blank=True, max_length=64, verbose_name='意向岗位')
	city = models.CharField(null=True, blank=True, max_length=16, verbose_name='意向城市')
	salary = models.CharField(null=True, blank=True, max_length=16, verbose_name='期望薪资')
	education = models.TextField(null=True, blank=True, verbose_name='教育经历')
	project = models.TextField(null=True, blank=True, verbose_name='项目经历')
	school_experience = models.TextField(null=True, blank=True, verbose_name='在校经历')
	self_introduction = models.TextField(null=True, blank=True, verbose_name='自我介绍')
	skill = models.TextField(null=True, blank=True, verbose_name='相关技能')
	honor = models.TextField(null=True, blank=True, verbose_name='荣誉证书')
	# 上传简历
	resume = models.FileField(upload_to="resume",null=True,blank=True,verbose_name="简历")

	class Meta:
		db_table = "hunter"


# # 投递之后的进度表
# # 投递状态
# SEND_STATUS = (
# 	(0, '已投递'),
# 	(1, '被查看'),
# 	(2, '接受面试邀请'),
# 	(3, '不符合'),
# 	(4, '拒绝面试邀请'),
# 	(5, '面试通过'),
# 	(6, '面试未通过'),
# 	(7, '收到聘用协议'),
# )


# class Process(models.Model):
# 	# 职位、投递时间、状态
# 	name = models.ForeignKey(to=Job_table, on_delete=models.CASCADE)
# 	time = models.DateTimeField(verbose_name='投递时间')
# 	send_status = models.IntegerField(choices=SEND_STATUS, verbose_name='投递状态')
#
# 	class Meta:
# 		db_table = "process"
