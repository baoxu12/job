from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from email.mime.text import MIMEText
from .models import *
import hashlib, random, datetime, smtplib


# Create your views here.

## 登录装饰器
def LoginVaild(func):
	## 1. 获取cookie中username和email
	## 2. 判断username和email
	## 3. 如果成功  跳转
	## 4. 如果失败   login.html
	def inner(request, *args, **kwargs):
		useremail = request.COOKIES.get('useremail')
		usertype = request.COOKIES.get("usertype")
		## 获取session
		session_useremail = request.session.get("useremail")
		session_type = request.session.get("usertype")
		if useremail and session_useremail and usertype and session_type and useremail == session_useremail and usertype == session_type and Boss.objects.filter(
				email=useremail, type=usertype).first():
			return func(request, *args, **kwargs)
		else:
			return HttpResponseRedirect('/login/')

	return inner


## 密码加密
def setPassword(password):
	## 实现一个密码加密
	md5 = hashlib.md5()  ## 创建一个md5的实例对象
	md5.update(password.encode())  ## 进行加密
	result = md5.hexdigest()
	return result


# 发送邮件
def send_email(email, subject, content):
	subject = subject
	content = content
	sender = "bx1125666@163.com"
	rec = email
	password = "bx19980105bx"
	###  MIMEText 参数 发送内容， 内容类型 , 编码
	message = MIMEText(content, "plain", "utf-8")
	message["Subject"] = subject
	message["From"] = sender
	message["To"] = rec

	smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
	smtp.login(sender, password)
	## 参数说明：发件人，收件人(一个列表/单个)     发送邮件 类似一种json的格式
	smtp.sendmail(sender, rec, message.as_string())
	smtp.close()
	result = {"code": 10000, "msg": "面试邀请已发送"}
	return result


# 获取当前登录用户
@LoginVaild
def get_user(request):
	useremail = request.COOKIES.get('useremail')
	usertype = request.COOKIES.get("usertype")
	user = Boss.objects.filter(email=useremail, type=usertype).first()
	return user


## 登出
@LoginVaild
def logout(request):
	response = HttpResponseRedirect("/login/")
	keys = request.COOKIES.keys()
	for one in keys:
		response.delete_cookie(one)

	del request.session['useremail']
	del request.session['usertype']
	return response


# 主页
@LoginVaild
def index(request, page):
	page = int(page)
	user = get_user(request)
	job = Job.objects.filter(b_boss_id=user.id).all()
	# 主页显示为投递简历未面试邀请的或者未点击不合适的；可操作邀请或者拒绝
	job_obj = Job_table.objects.filter(j_name__in=job, send_status__lte=2).order_by("time")

	job_all = Paginator(job_obj, 10)
	job_list = job_all.page(page)
	current_page = job_list.number
	start = current_page - 3
	if start < 1:
		start = 0
	end = current_page + 2
	if end > job_all.num_pages:
		end = job_all.num_pages
	if start == 0:
		end = 5
	page_range = job_all.page_range[start:end]

	return render(request, "boss/index.html", locals())


# 个人信息页
@LoginVaild
# 个人信息页
def boss_info(request):
	user = get_user(request)
	work_status = user.get_work_status_display()
	if request.method == "POST":
		# 	# 获取表单信息，存入数据库
		data = request.POST
		user.name = data.get("name")
		user.phone = data.get("phone")
		user.age = data.get("age")
		user.gender = data.get("gender")
		user.address = data.get("address")
		user.photo = request.FILES.get('photo')
		user.save()
	return render(request, "boss/boss_info.html", locals())


# 资历资料
def record(request):
	user = get_user(request)
	company = Company.objects.all()
	if request.method == "POST":
		data = request.POST
		user.work_status = int(data.get("work_status"))
		user.professional_title = data.get("professional_title")
		user.work_experience = data.get("work_experience")
		c_id = data.get("company")
		try:
			if int(c_id):
				user.b_company = Company.objects.get(id=int(c_id))
		except:
			pass
		user.save()
	return render(request, 'boss/record.html', locals())


# 修改密码
def update(request):
	user = get_user(request)
	if request.method == "POST":
		data = request.POST
		update = data.get("update_password")
		update1 = data.get("update_password1")
		if update and update1 and update == update1:
			user.password = setPassword(update)
			user.save()
	return render(request, 'boss/update_password.html', locals())


# 增加公司/完善公司信息
def company(request):
	user = get_user(request)
	c_type = C_type.objects.all()
	if request.method == "POST":
		data = request.POST
		try:
			company = Company.objects.get(id=Boss.objects.filter(email=user.email, type=user.type).first().b_company_id)
			company.c_email = data.get("email")
			company.phone_number = data.get("phone")
			company.c_legal = data.get("legal")
			company.c_status = int(data.get("status"))
			company.c_staff = data.get("staff")
			company.c_scope = data.get("scope")
			company.c_website = data.get("website")
			company.c_descript = data.get("descript")
			company.save()

		except:
			company = Company()
			company.c_email = data.get("email")
			company.c_name = data.get("name")
			company.phone_number = data.get("phone")
			company.c_code = data.get("code")
			company.c_legal = data.get("legal")
			company.c_money = int(data.get("money"))
			company.c_status = int(data.get("status"))

			date_str = data.get("time")
			company.c_time = datetime.date(*map(int, date_str.split('-')))
			company.c_address = data.get("address")
			company.c_scope = data.get("scope")
			company.c_website = data.get("website")
			company.c_descript = data.get("descript")
			company.c_photo = request.FILES.get("photo")
			company.c_staff = data.get("staff")

			data_type = data.get("data_type")
			try:
				if int(data_type):
					company.c_type_id = int(data_type)
			except:
				type_name = data.get("type")
				if type_name:
					t = C_type()
					t.type = type_name
					t.save()
					company.c_type = C_type.objects.get(type=type_name)
			company.save()
			user.b_company_id = company.id
			user.save()
	return render(request, 'boss/company.html', locals())


# 发布职位
def job_publish(request):
	user = get_user(request)
	city = City.objects.all()
	if request.method == "POST":
		data = request.POST
		job = Job()
		job.job_name = data.get("job_name")
		job.job_address = data.get("job_address")
		job.education = int(data.get("education"))
		job.pay = data.get("pay")
		job.job_descript = data.get("job_descript")
		job.demand = data.get("demand")
		job.work_time = data.get("work_time")
		job.job_label = data.get("job_label").split("；")
		data_city = data.get("data_city")
		try:
			if int(data_city):
				job.city_id = int(data_city)
		except:
			city_name = data.get("city")
			if city_name:
				c = City()
				c.name = city_name
				c.save()
				job.city = City.objects.get(name=city_name)
		job.check_status = 0
		job.j_company_id = user.b_company.id
		job.b_boss_id = user.id
		job.save()

	return render(request, 'boss/job_publish.html', locals())


# 职位状态页
def job_list(request, status, page):
	"""
		传入参数介绍
		:param request:
		:param status:0，1，2，3
		:param page:页数
		:return:待审核，审核中，已发布，审核未通过
		"""
	user = get_user(request)
	page = int(page)
	if status == "0":
		## 待审核
		job_obj = Job.objects.filter(check_status=0, b_boss_id=user.id).order_by("time")
	elif status == "1":
		## 审核中
		job_obj = Job.objects.filter(check_status=1, b_boss_id=user.id).order_by("time")
	elif status == "2":
		## 已发布
		job_obj = Job.objects.filter(check_status=2, b_boss_id=user.id).order_by("time")
	elif status == "3":
		## 审核未通过
		job_obj = Job.objects.filter(check_status=3, b_boss_id=user.id).order_by("time")
	job_all = Paginator(job_obj, 10)
	job_list = job_all.page(page)
	current_page = job_list.number
	start = current_page - 3
	if start < 1:
		start = 0
	end = current_page + 2
	if end > job_all.num_pages:
		end = job_all.num_pages
	if start == 0:
		end = 5
	page_range = job_all.page_range[start:end]

	return render(request, 'boss/job_list.html', locals())


# 查看/修改职位信息
def check(request):
	user = get_user(request)
	id = request.GET.get("id")
	job = Job.objects.get(id=int(id))
	education = job.get_education_display()
	city = City.objects.all()
	if request.method == "POST":
		data = request.POST
		job.job_name = data.get("job_name")
		job.job_address = data.get("job_address")
		job.education = int(data.get("education"))
		job.pay = data.get("pay")
		job.job_descript = data.get("job_descript")
		job.demand = data.get("demand")
		job.work_time = data.get("work_time")
		job.job_label = data.get("job_label")
		data_city = data.get("data_city")
		try:
			if int(data_city):
				job.city_id = int(data_city)
		except:
			city_name = data.get("city")
			if city_name:
				c = City()
				c.name = city_name
				c.save()
				job.city = City.objects.get(name=city_name)
		job.check_status = 0
		job.save()

	return render(request, 'boss/job_detail.html', locals())


# 删除职位
def delete_job(request):
	if request.method == "POST":
		data = request.POST
		d_id = data.get("d_id")
		job = Job.objects.get(id=d_id)
		job.delete()
		result = {"code": 10000, "msg": "删除成功"}
	return JsonResponse(result)


# 求职者投递简历后，boss操作状态
def send_status(request, status, page):
	page = int(page)
	user = get_user(request)
	job = Job.objects.filter(b_boss_id=user.id).all()
	if status == "0":
		## 未查看
		job_obj = Job_table.objects.filter(send_status=0, j_name__in=job).order_by("time")
	elif status == "1":
		## 已查看
		job_obj = Job_table.objects.filter(send_status__gte=1, j_name__in=job).order_by("time")
	elif status == "2":
		## 已发送邀请
		job_obj = Job_table.objects.filter(send_status__in=[2, 3, 5, 6, 7, 8], j_name__in=job).order_by("time")
	elif status == "3":
		## 面试邀请成功
		job_obj = Job_table.objects.filter(send_status__in=[3, 6, 7, 8], j_name__in=job).order_by("time")
	elif status == "4":
		## 不合适
		job_obj = Job_table.objects.filter(send_status=4, j_name__in=job).order_by("time")
	elif status == "5":
		## 邀请面试失败
		job_obj = Job_table.objects.filter(send_status=5, j_name__in=job).order_by("time")
	elif status == "6":
		## 面试通过
		job_obj = Job_table.objects.filter(send_status__in=[6,8], j_name__in=job).order_by("time")
	elif status == "7":
		## 面试未通过
		job_obj = Job_table.objects.filter(send_status=7, j_name__in=job).order_by("time")
	elif status == "8":
		## 录用通知已发送
		job_obj = Job_table.objects.filter(send_status=8, j_name__in=job).order_by("time")
	job_all = Paginator(job_obj, 10)
	job_list = job_all.page(page)
	current_page = job_list.number
	start = current_page - 3
	if start < 1:
		start = 0
	end = current_page + 2
	if end > job_all.num_pages:
		end = job_all.num_pages
	if start == 0:
		end = 5
	page_range = job_all.page_range[start:end]

	return render(request, 'boss/send_status.html', locals())


def invate(request):
	user = get_user(request)
	i_id = request.GET.get("i_id")
	f_id = request.GET.get("f_id")
	s_id = request.GET.get("s_id")
	# 录用协议
	if s_id:
		jt = Job_table.objects.get(id=int(s_id))
		job = jt.j_name.job_name
		company_name = jt.j_name.j_company.c_name
		recv_name = jt.h_name.name
		recv_email = jt.h_name.email
	# 面试邀请
	if i_id:
		jt = Job_table.objects.get(id=int(i_id))
		job = jt.j_name.job_name
		company_name = jt.j_name.j_company.c_name
		recv_name = jt.h_name.name
		recv_email = jt.h_name.email
	# 不合适
	if f_id:
		jt = Job_table.objects.get(id=int(f_id))
		job = jt.j_name.job_name
		company_name = jt.j_name.j_company.c_name
		recv_name = jt.h_name.name
		recv_email = jt.h_name.email
	page = request.GET.get("page")
	return render(request, "boss/invated.html", locals())


# 对于收到简历的各种操作
def operate(request):
	if request.method == "POST":
		data = request.POST
		check_id = data.get("check_id")
		invate_id = data.get("invate_id")
		fail_id = data.get("fail_id")
		failed_id = data.get("failed_id")
		p_id = data.get("p_id")
		send_id = data.get("send_id")
		# 发送录用通知
		if send_id:
			try:
				invate_time = data.get("time").replace("T", " ")
			except:
				invate_time = ""
			address = data.get("address")
			jt = Job_table.objects.get(id=int(send_id))
			comapny_name = jt.j_name.j_company.c_name
			# 职位名称
			job_name = jt.j_name.job_name
			# 求职者名字
			recv_name = jt.h_name.name
			# 求职者邮箱
			recv_email = jt.h_name.email
			job_pay = jt.j_name.pay
			hr_phone = jt.j_name.b_boss.phone
			content = "%s 先生/小姐：\n 您好！ \n 您诚意应聘本公司%s职位，经初审合格，依本公司任用规定给予录取，谒诚欢迎您加入本公司行列。有关报到事项如下，敬请参照办理。 \n 　一、报到日期：%s \n 地点：%s \n 二、携带资料：\n (一)录用通知书; \n (二)居民身份证;\n (三)最高学历证书原件;\n (四)体检合格证明(区以上医院体验证明); \n (五)非本市户口需携带外出就业证明; \n (六)一寸相片三张; \n  三、薪资：%s　\n 四、前列事项若有疑问或困难，请与本公司人事部联系：\n 电话：%s \n %s人事部" % (
				recv_name, job_name, invate_time, address, job_pay, hr_phone, comapny_name)
			subject = comapny_name + job_name + "录用通知"
			send_email(recv_email, subject, content)
			jt.send_status = 8
			jt.save()
			result = {"code": 10000, "msg": "录用通知发送成功"}
		# 面试通过
		if p_id:
			jt = Job_table.objects.get(id=int(p_id))
			comapny_name = jt.j_name.j_company.c_name
			company_website = jt.j_name.j_company.c_website
			b_name = jt.j_name.b_boss.name
			# 职位名称
			job_name = jt.j_name.job_name
			# 求职者名字
			recv_name = jt.h_name.name
			# 求职者邮箱
			recv_email = jt.h_name.email
			content = "%s 先生/小姐：\n 您好！ \n 我是%s的人事%s，很高兴地通知您，您应聘的%s职位已面试合格，稍后会向您发送录用邮件 \n " % (
				recv_name, comapny_name, b_name, job_name)
			subject = comapny_name + job_name + "面试结果通知函"
			send_email(recv_email, subject, content)
			jt.send_status = 6
			jt.save()
			result = {"code": 10000, "msg": "面试结果发送成功"}
		# 面试未通过
		if failed_id:
			jt = Job_table.objects.get(id=int(failed_id))
			comapny_name = jt.j_name.j_company.c_name
			company_website = jt.j_name.j_company.c_website
			# 职位名称
			job_name = jt.j_name.job_name
			# 求职者名字
			recv_name = jt.h_name.name
			# 求职者邮箱
			recv_email = jt.h_name.email
			content = "%s 先生/小姐：\n 您好！ \n 感谢您参加本公司%s的面试！ \n 对您在面试过程中所表现出来的积极努力和认真参与的态度,我们谨致以由衷的敬意和真诚的赞赏！ \n 您已经是表现出优秀的才能,才在众人之中脱颖而出参与我们的面试阶段,在面试当中您更是表现出了许多方面的特殊潜质。但经过慎重的考虑和评估,觉得您暂时不适合这个职位,但是我们对您仍然是充满了信心和敬意,相信您会找到更加适合您的舞台,我们由衷地祝福您。 \n 您的相关资料已存入我公司储备人才库中,日后的招聘职位中可能会有适合的职位,欢迎继续关注我们的招聘信息%s \n 再次感谢!相信您一定可以找到最适合您的发展之处! \n 祝您在将来的日子里,每天拥有愉快的生活! \n %s人事部" % (
				recv_name, job_name, company_website, comapny_name)
			subject = comapny_name + job_name + "面试结果通知函"
			send_email(recv_email, subject, content)
			jt.send_status = 7
			jt.save()
			result = {"code": 10000, "msg": "面试结果通知成功"}
		# 查看简历
		if check_id:
			jt = Job_table.objects.get(id=int(check_id))
			if jt.send_status == 0:
				jt.send_status = 1
				jt.save()
				result = {"code": 10000, "msg": "查看"}
			else:
				result = {"code": 10000, "msg": "已查看"}
		# 面试邀请
		if invate_id:
			try:
				invate_time = data.get("time").replace("T", " ")
			except:
				invate_time = ""
			address = data.get("address")
			jt = Job_table.objects.get(id=int(invate_id))
			# 公司名称
			comapny_name = jt.j_name.j_company.c_name
			# 职位名称
			job_name = jt.j_name.job_name
			# 求职者名字
			recv_name = jt.h_name.name
			# 求职者邮箱
			recv_email = jt.h_name.email
			# hr
			hr_name = jt.j_name.b_boss.name
			hr_phone = jt.j_name.b_boss.phone
			if jt.send_status < 2:
				# 发送面试邀请邮件
				content = "%s 先生/小姐：\n 您好！ \n 很高兴收到您的简历，您的简历已通过我司初次筛选，为了能增进彼此进一步了解，现诚邀您至我司初次筛选，具体事宜如下，若有疑问或需改期请及时与我联系，谢谢。 \n 面试职位：%s \n 面试时间：%s \n 公司地址：%s    \n 联系人：%s先生 \n 联系电话：%s " % (
					recv_name, job_name, invate_time, address, hr_name, hr_phone)
				send_email(recv_email, comapny_name, content)
				jt.send_status = 2
				jt.save()
				result = {"code": 10000, "msg": "面试邀请已发送"}
			else:
				content = "%s 先生/小姐：\n 您好！ \n 很高兴收到您的简历，您的简历已通过我司初次筛选，为了能增进彼此进一步了解，现诚邀您至我司初次筛选，具体事宜如下，若有疑问或需改期请及时与我联系，谢谢。 \n 面试职位：%s \n 面试时间：%s \n 公司地址：%s    \n 联系人：%s先生 \n 联系电话：%s " % (
					recv_name, job_name, invate_time, address, hr_name, hr_phone)
				subject = comapny_name + job_name + "面试邀请函"
				send_email(recv_email, subject, content)
				result = {"code": 10000, "msg": "再次发送面试邀请"}
		# 不合适
		elif fail_id:

			refuse = data.get("refuse")
			jt = Job_table.objects.get(id=int(fail_id))
			comapny_name = jt.j_name.j_company.c_name
			# 职位名称
			job_name = jt.j_name.job_name
			# 求职者名字
			recv_name = jt.h_name.name
			# 求职者邮箱
			recv_email = jt.h_name.email
			if jt.send_status < 2:
				# 发送邮件投递失败
				content = "%s 先生/小姐：\n 您好！ \n 非常抱歉，由于%s，您未通过我们的初次审核。别灰心，您已进入我司人才储备，期待未来有机会再见到您。感谢您的投递! \n 应聘公司：%s \n 应聘岗位：%s \n 反馈结果：不合适" % (
					recv_name, refuse, comapny_name, job_name)
				subject = "反馈通知：" + comapny_name + job_name
				send_email(recv_email, subject, content)
				jt.send_status = 4
				jt.save()
				result = {"code": 10001, "msg": "邮件发送成功"}
	return JsonResponse(result)

def add_job(request):
	job_name_list = ["爬虫工程师","系统测试师","UI设计师","java开发工程师","数据分析","前端工程师","安卓工程师","苹果工程师","网络安全工程师","后端工程师","运维工程师","项目经理"]
	job_shanghai_list=["上海市黄浦区","上海市静安区","上海市徐汇区","上海市长宁区","上海市杨浦区","上海市虹口区","上海市普陀区","上海市浦东新区","上海市宝山区","上海市嘉定区","上海市闵行区","上海市松江区"]
	job_beijing_list = ["北京市东城区","北京市西城区","北京市宣武区","北京市崇文区","北京市朝阳区","北京市丰台区"]
	job_guangzhou_list = ["广州市越秀区","广州市荔湾区","广州市增城区","广州市海珠区","广州市天河区"]
	job_wuhan_list = ["武汉市江汉区","武汉市硚口区","武汉市江岸区","武汉市汉阳区","武汉市武昌区"]
	job_shenzhen_list = ["深圳市罗湖区","深圳市福田区","深圳市南山区","深圳市宝安区","深圳市龙岗区"]
	job_hanzghou_list = ["杭州市临安区", "杭州市西湖区", "杭州市上城区", "杭州市滨江区", "杭州市余杭区"]
	job_nanjing_list = ["南京市玄武区", "南京市六合区", "南京市浦口区", "南京市江宁区", "南京市秦淮区"]
	job_huangshan_list = ["黄山市屯溪区", "黄山市黄山区", "黄山市徽州区"]
	education_list = [0,1,2,3]
	pay_list = ["9k","10k","8k","7k","6k","11k","12k"]
	job_label_list = [['五险一金', '定期体检', '年终奖', '股票期权', '带薪年假', '员工旅游'],['五险一金', '定期体检',  '带薪年假', '员工旅游', '节日福利'],[ '年终奖', '股票期权', '带薪年假', '员工旅游', '节日福利', '零食下午茶'],['五险一金', '股票期权', '带薪年假', '员工旅游', '节日福利', '零食下午茶']]


	# for i in range(5):
	# 	job = Job()
	# 	job.job_name = random.choice(job_name_list)

	#
	#
	# 	job.job_address = random.choice(job_huangshan_list)
	#
	#
	# 	job.education = random.choice(education_list)
	# 	job.pay = random.choice(pay_list)
	# 	job.job_descript = "1、参与需求分析，产品设计，功能开发；2、承担Web后端开发工作，开发并维护服务器端及数据管理后台；3、配合AI工程师进行数据处理等相关工作。"
	# 	job.demand = "1、熟练掌握python3语言进行服务端开发；2、熟悉tornado、Django、flask框架中一种，构建过nginx + uWSGI + python的web-services者优先；3、熟悉面向对象编程，熟悉Python设计模式，有一定的逻辑思维能力；4、对Python多线程、多进程方面有丰富经验者优先；5、掌握一定的web前端技能，了解或熟悉HTML、CSS、Javascript；6、熟悉关系型数据库开发与优化；7、熟悉Linux操作系统，了解Apache/Ngnix等Web Server的部署和应用；8、有大型网络服务开发，在高并发，高稳定性方面有经验者优先考虑；9、会其他编程语言如Java、NodeJS者优先。"
	# 	job.work_time = "周一至周五：早(8:00~11:30),午(1:30~6:00)"
	# 	job.job_label = random.choice(job_label_list)
	# 	job.check_status = 0
	#
	#
	# 	job.city_id = 11
	#
	#
	# 	job.j_company_id = 2
	# 	job.b_boss_id = 1
	# 	job.save()


	return HttpResponse("增加职位成功")