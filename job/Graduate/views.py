import random, hashlib, requests, re, PyPDF2, datetime

from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from Boss.models import *

import geoip2.database


# Create your views here.

## 登录装饰器
def LoginVaild(func):
	def inner(request, *args, **kwargs):
		useremail = request.COOKIES.get('useremail')
		usertype = request.COOKIES.get("usertype")
		## 获取session
		session_useremail = request.session.get("useremail")
		session_type = request.session.get("usertype")
		if useremail and session_useremail and usertype and session_type and useremail == session_useremail and usertype == session_type and Hunter.objects.filter(
				email=useremail, type=usertype).first():
			return func(request, *args, **kwargs)
		else:
			return HttpResponseRedirect('/login/')

	return inner


# 获取当前登录用户
@LoginVaild
def get_user(request):
	useremail = request.COOKIES.get('useremail')
	usertype = request.COOKIES.get("usertype")
	user = Hunter.objects.filter(email=useremail, type=usertype).first()
	return user


# 获取当前ip所在城市
def get_city():
	# 通过requests请求ip网址，re匹配来获取外网ip，来获取城市名
	while True:
		url = "https://ip.cn/"
		headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
		}
		html_text = requests.get(url, headers=headers).text
		try:
			ip = re.search("<p>您现在的 IP：<code>(.*?)</code></p>", html_text)
			reader = geoip2.database.Reader('GeoLite2-City/GeoLite2-City.mmdb')
			data = reader.city(ip.group(1))
			city_name = data.city.names['zh-CN']
		except:
			city_name = ''
		if city_name:
			break
	city = City.objects.all()
	city_list = [one.name for one in city]
	if city_name in city_list:
		c_id = City.objects.get(name=city_name).id
	else:
		c_id = ""

	return city_name,c_id


## 密码加密
def setPassword(password):
	## 实现一个密码加密
	md5 = hashlib.md5()  ## 创建一个md5的实例对象
	md5.update(password.encode())  ## 进行加密
	result = md5.hexdigest()
	return result


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
def index(request):
	user = get_user(request)
	ct_id = request.GET.get("ct_id")
	city = City.objects.all()
	if ct_id:
		city_name = City.objects.get(id=int(ct_id)).name
		job_obj = Job.objects.filter(check_status=2, city_id=int(ct_id)).order_by("time")
		if job_obj:
			job = job_obj
		else:
			job = Job.objects.filter(check_status=2).order_by("time")
	else:
		city_name,c_id = get_city()
			# 展示数据未职位
		# 说明定位城市存在，那么展示该城市职位
		if c_id:
			job_obj = Job.objects.filter(check_status=2, city_id=c_id).order_by("time")
			if job_obj:
				job = job_obj
			else:
				job = Job.objects.filter(check_status=2).order_by("time")
		else:
			city_name = city_name
			job = Job.objects.filter(check_status=2).order_by("time")
	return render(request, "graduate/index.html", locals())


# 个人信息页
@LoginVaild
def userinfo(request):
	user = get_user(request)
	resume = user
	if request.method == "POST":
		# 	# 获取表单信息，存入数据库
		data = request.POST
		user.name = data.get("name")
		user.phone = data.get("phone")
		user.age = data.get("age")
		user.gender = data.get("gender")
		user.native = data.get("address")
		user.photo = request.FILES.get('photo')
		user.resume = request.FILES.get("resume")
		user.save()

	return render(request, 'graduate/userinfo.html', locals())


# 修改密码
@LoginVaild
def update(request):
	user = get_user(request)
	if request.method == "POST":
		data = request.POST
		update = data.get("update_password")
		update1 = data.get("update_password1")
		if update and update1 and update == update1:
			user.password = setPassword(update)
			user.save()
	return render(request, 'graduate/update_password.html', locals())


# 在线编写简历
@LoginVaild
def resume(request):
	user = get_user(request)
	resume = user
	if request.method == "POST":
		# 	# 获取表单信息，存入数据库
		data = request.POST
		resume.expect_job = data.get("job")
		resume.city = data.get("city")
		resume.salary = data.get("salary")
		resume.education = data.get("education")
		resume.project = data.get("project")
		resume.school_experience = data.get("school_experience")
		resume.skill = data.get("skill")
		resume.honor = data.get("honor")
		resume.self_introduction = data.get("self_introduction")
		resume.save()

	return render(request, 'graduate/resume.html', locals())


# 公司信息页
def company_info(request):
	user = get_user(request)
	job_id = request.GET.get("job_id")
	print(job_id)
	c_id = request.GET.get("c_id")
	job = Job.objects.get(id=job_id)
	company = Company.objects.get(id=c_id)
	return render(request, 'graduate/company_info.html', locals())


# 职位信息页
def job_info(request):
	user = get_user(request)
	j_id = request.GET.get("j_id")
	job = Job.objects.get(id=j_id)
	desc = job.job_descript.split("；")
	demand = job.demand.split("；")
	try:
		jt = Job_table.objects.get(h_name_id=user.id,j_name=job)
	except:
		jt = ""
	return render(request, 'graduate/job_info.html', locals())


# 投递简历
def send_resume(request):
	user = get_user(request)
	j_id = request.GET.get("j_id")
	if request.method == "POST":
		type = request.POST.get("type")
		if type and type == "exist":
			t = Job_table()
			t.h_name_id = user.id
			t.j_name_id = Job.objects.get(id=int(j_id)).id
			t.time = datetime.datetime.now()
			t.send_status = 0
			t.save()
			result = {"code": 10000, "msg": "投递成功"}
		else:
			data = request.FILES.get("file")
			hunter = Hunter.objects.get(id=user.id)
			hunter.resume = data
			hunter.save()
			# 存进boss页面的Job_table表
			t = Job_table()
			t.h_name_id = user.id
			# 职位名
			t.j_name_id = Job.objects.get(id=int(j_id)).id
			t.time = datetime.datetime.now()
			t.send_status = 0
			t.save()
			result = {"code": 10000, "msg": "投递成功"}
	# hunter = Hunter.objects.get(id=user.id)
	# file = hunter.resume
	# filename = file.name
	# try:
	# 	result = filename.split('.')[1]
	# except:
	# 	result = "docx"
	# if result.lower() == "pdf":
	# 	# pdf文件
	# 	pdf_file = open('./static/{}'.format(filename), 'rb')
	# 	pdfReader = PyPDF2.PdfFileReader(pdf_file)
	#
	# 	pdfWriter = PyPDF2.PdfFileWriter()
	# 	for pageNum in range(pdfReader.numPages):
	# 		pageObj = pdfReader.getPage(pageNum)
	# 		pdfWriter.addPage(pageObj)
	# 	pdf_put = open('./static/upload_files/{}'.format(filename), 'wb')
	# 	pdfWriter.write(pdf_put)
	# 	pdf_put.close()
	# 	pdf_file.close()
	# else:
	# 	if file.size == "0":
	# 		message = "上传文件不能为空"
	# 	else:
	# 		# docx文件
	# 		with open("./static/upload_files/{}".format(filename),'wb+') as f:
	# 			string = file.read()
	# 			f.write(string)
	return JsonResponse(result)


def resume_status(request,status,page):
	page = int(page)
	user = get_user(request)

	if status == "0":
		# 已投递
		job_obj = Job_table.objects.filter(send_status__gte=0, h_name=user).order_by("time")
	elif status == "1":
		# 已查看
		job_obj = Job_table.objects.filter(send_status__gte=1, h_name=user).order_by("time")
	elif status == "2":
		# 收到面试邀请
		job_obj = Job_table.objects.filter(send_status__in=[2,3,5,6,7,8], h_name=user).order_by("time")
	elif status == "3":
		# 接受面试邀请
		job_obj = Job_table.objects.filter(send_status__in=[3,6,7,8], h_name=user).order_by("time")
	elif status == "4":
		# 不符合
		job_obj = Job_table.objects.filter(send_status=4, h_name=user).order_by("time")
	elif status == "5":
		## 拒绝面试邀请
		job_obj = Job_table.objects.filter(send_status=5, h_name=user).order_by("time")
	elif status == "6":
		## 面试通过
		job_obj = Job_table.objects.filter(send_status__in=[6,8], h_name=user).order_by("time")
	elif status == "7":
		## 面试未通过
		job_obj = Job_table.objects.filter(send_status=7, h_name=user).order_by("time")
	elif status == "8":
		## 收到录用通知
		job_obj = Job_table.objects.filter(send_status=8, h_name=user).order_by("time")
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


	return render(request,'graduate/resume_status.html',locals())

# 操作
def operate(request):
	if request.method == "POST":
		data = request.POST
		r_id = data.get("r_id")
		a_id = data.get("a_id")
		# 拒绝面试邀请
		if r_id:
			jt = Job_table.objects.get(id=r_id)
			jt.send_status = 5
			jt.save()
			result = {"code": 10000, "msg": "拒绝面试邀请成功"}
			# 接受面试邀请
		elif a_id:
			jt = Job_table.objects.get(id=a_id)
			jt.send_status = 3
			jt.save()
			result = {"code": 10000, "msg": "接受面试邀请"}
	return JsonResponse(result)
