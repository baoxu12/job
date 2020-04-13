from django.db import models

# Create your models here.

# 企业性质表
class C_type(models.Model):
	type = models.CharField(max_length=64,verbose_name="企业性质")

	class Meta:
		db_table = 'c_type'


# 企业表
# 经营状态
MANAGE_STATUS = (
	(0,"存续(开业、正常、登记)"),
	(1,"在业"),
	(2,"吊销"),
	(3,"注销"),
	(4,"迁出"),
	(5,"迁入"),
	(6,"停业"),
	(7,"清算"),
	)
# 职员人数
STAFF_NUM = (
	(0,"少于10人"),
	(1,"10-49人"),
	(2,"50-99人"),
	(3,"100-499人"),
	(4,"500-999人"),
	(5,"1000-9999人"),
	(6,"10000人以上")
)

class Company(models.Model):
	c_email = models.EmailField(verbose_name='企业邮箱')
	c_name = models.CharField(max_length=32, verbose_name='企业名')
	phone_number = models.CharField(max_length=11, verbose_name='企业电话')
	c_code = models.CharField(max_length=32,verbose_name='统一信用代码')
	c_legal = models.CharField(max_length=32,verbose_name='企业法人')
	c_photo = models.ImageField(upload_to='images', verbose_name='企业照片')
	# 注册资本,单位：万元
	c_money = models.IntegerField(verbose_name='注册资本')
	c_status = models.IntegerField(choices=MANAGE_STATUS,verbose_name='经营状态')
	c_time = models.DateField(verbose_name='成立时间')
	c_address = models.TextField(verbose_name='注册地址')
	c_scope = models.TextField(verbose_name='经营范围')
	c_website = models.TextField(verbose_name='公司官网')
	c_descript = models.TextField(verbose_name='公司简介')
	# 公司人员
	c_staff = models.IntegerField(null=True,blank=True,choices=STAFF_NUM,verbose_name='职员人数')
	# 外键公司性质
	c_type = models.ForeignKey(null=True,blank=True,to=C_type,on_delete=models.CASCADE)

	class Meta:
		db_table = 'company'

# 招聘者现工作岗位信息
# 在职信息
WORK_STATUS = (
	(0,'在职'),
	(1,'离职'),
	(2,'停职'),
)

# 招聘者表
class Boss(models.Model):
	email = models.EmailField(verbose_name='邮箱', default=0)
	password = models.CharField(max_length=32, verbose_name='密码')
	name = models.CharField(max_length=32, null=True, blank=True, verbose_name='招聘者名')
	## null 针对数据库，可以为空
	## blank针对表单，表示在表单中该字段可以不填，对数据库没有影响
	phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
	## type 中
	## 0 代表求职者
	## 1 代表企业
	## 2 代表管理员
	type = models.CharField(max_length=4,null=True, blank=True, verbose_name='类别')
	photo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='头像')
	age = models.IntegerField(null=True, blank=True, verbose_name='年龄')
	gender = models.CharField(max_length=4, null=True, blank=True, verbose_name='性别')
	address = models.TextField(null=True, blank=True, verbose_name='居住地')
	work_status = models.IntegerField(null=True, blank=True,choices=WORK_STATUS, verbose_name='在职信息')
	professional_title = models.CharField(null=True, blank=True, max_length=32, verbose_name='职称')
	work_experience = models.TextField(null=True, blank=True, verbose_name='工作经验')
	# 外键，对应公司
	b_company = models.ForeignKey(null=True,blank=True,to=Company,on_delete=models.CASCADE)

	class Meta:
		db_table = 'boss'

# 城市表
class City(models.Model):
	name = models.CharField(max_length=32)

	class Meta:
		db_table = 'city'


# 职位表
# 学历
EDUCATION = (
	(0,'大专'),
	(1,'本科'),
	(2,'硕士'),
	(3,'博士'),
)
# 审核状态
REVIEW_STATUS = (
	(0,"待审核"),
	(1,"审核中"),
	(2,"已发布"),
	(3,"审核未通过"),
	(4,"已删除"),
	)

class Job(models.Model):
	job_name = models.CharField(max_length=32, verbose_name='职位名称')
	job_address = models.TextField(verbose_name='工作地点')
	education = models.IntegerField(choices=EDUCATION,verbose_name='学历')
	pay = models.CharField(max_length=20,verbose_name='薪资')
	job_descript = models.TextField(null=True,blank=True,verbose_name='岗位详情')
	demand = models.TextField(verbose_name='任职要求')
	work_time = models.TextField(verbose_name='工作时间')
	# 发布时间
	time = models.DateTimeField(auto_now=True,null=True,blank=True,verbose_name='发布时间')
	# 职位诱惑/标签   注意：在文本框中必须以逗号分割
	job_label = models.TextField(verbose_name='标签')
	# 管理员审核状态
	check_status = models.IntegerField(null=True, blank=True, choices=REVIEW_STATUS, verbose_name="审核状态")
	# 外键，对应城市,改职位在哪个城市下
	city = models.ForeignKey(to=City,on_delete=models.CASCADE,default=1)
	# 外键，对应公司
	j_company = models.ForeignKey(to=Company,on_delete=models.CASCADE)
	# 外键，对应hr
	b_boss = models.ForeignKey(to=Boss,on_delete=models.CASCADE)

	class Meta:
		db_table = 'job'

# 职位下投递情况表
# 投递状态
SEND_STATUS = (
	(0,'未查看'),
	(1,'已查看'),
	(2,'已发送邀请'),
	(3,'邀请面试成功'),
	(4,'不合适'),
	(5,'邀请面试失败'),
	(6,'面试通过'),
	(7,'面试未通过'),
	(8,'录用通知已发送'),
)

class Job_table(models.Model):
	# 投递者
	h_name = models.ForeignKey(to="Graduate.Hunter",on_delete=models.CASCADE)
	# 职位名
	j_name = models.ForeignKey(to=Job,on_delete=models.CASCADE,null=True,blank=True)
	time = models.DateTimeField(verbose_name='投递时间')
	send_status = models.IntegerField(choices=SEND_STATUS,verbose_name='投递状态')

	class Meta:
		db_table = 'job_table'

