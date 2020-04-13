from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from Graduate.models import Hunter
from Boss.models import Boss
from .models import *
import hashlib


# Create your views here.

## 管理员的主页应该有：1.管理员个人信息页面，2.求职者的信息页面，3.企业的信息页面

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
		if useremail and session_useremail and usertype and session_type and useremail == session_useremail and usertype == session_type and Admins.objects.filter(
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


# 获取当前登录用户
@LoginVaild
def get_user(request):
	useremail = request.COOKIES.get('useremail')
	usertype = request.COOKIES.get("usertype")
	user = Admins.objects.filter(email=useremail, type=usertype).first()
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
def index(request,page):
	page = int(page)
	user = get_user(request)
	job_obj = Job.objects.filter(check_status=0).all()
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

	return render(request, "adm/index.html", locals())

# 查看发布职位
def job_check(request):
	user = get_user(request)
	id = request.GET.get("id")
	job = Job.objects.get(id=int(id))
	if job.check_status == 0:
		job.check_status = 1
		job.save()

	return render(request,'adm/job_check.html',locals())

# 职位操作
def check_operation(request):
	if request.method == "POST":
		data = request.POST
		fb_id = data.get("fb_id")
		bh_id = data.get("bh_id")
		sc_id = data.get("sc_id")
		if fb_id:
			job = Job.objects.get(id=int(fb_id))
			job.check_status = 2
			job.save()
			result = {"code": 10000, "msg": "发布成功"}
		elif bh_id:
			job = Job.objects.get(id=int(bh_id))
			job.check_status = 3
			job.save()
			result = {"code": 10000, "msg": "驳回成功"}
		elif sc_id:
			job = Job.objects.get(id=int(sc_id))
			job.check_status = 4
			job.save()
			result = {"code": 10000, "msg": "删除成功"}
		result = result
	return JsonResponse(result)


@LoginVaild
# 个人信息页
def adm_info(request):
	user = get_user(request)
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
	return render(request, "adm/adm_info.html", locals())


# 求职者管理
def hunter(request, page=1):
	user = get_user(request)
	page = int(page)
	hunter = Hunter.objects.all()
	paginator = Paginator(hunter, 8)
	page_obj = paginator.page(page)
	current_page = page_obj.number
	start = current_page - 3
	if start < 1:
		start = 0
	end = current_page + 2
	if end > paginator.num_pages:
		end = paginator.num_pages
	if start == 0:
		end = 5
	page_range = paginator.page_range[start:end]
	return render(request, "adm/adm_hunter.html", locals())


# 企业管理
def boss(request,page):
	user = get_user(request)
	page = int(page)
	boss = Boss.objects.all()
	paginator = Paginator(boss, 8)
	page_obj = paginator.page(page)
	current_page = page_obj.number
	start = current_page - 3
	if start < 1:
		start = 0
	end = current_page + 2
	if end > paginator.num_pages:
		end = paginator.num_pages
	if start == 0:
		end = 5
	page_range = paginator.page_range[start:end]
	return render(request, "adm/adm_boss.html",locals())


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
	return render(request, 'adm/update_password.html', locals())


# 查看或修改信息
def operation(request):
	user = get_user(request)
	id = request.GET.get("id")
	type = request.GET.get("type")
	if type == "0":
		member = Hunter.objects.filter(id=int(id),type=type).first()
	elif type == "1":
		member = Boss.objects.filter(id=int(id),type=type).first()
	member = member
	if request.method == "POST":
		data = request.POST
		# 	# 获取表单信息，存入数据库
		password = data.get("password")
		if password:
			member.password = setPassword(password)
		else:
			member.password = member.password
		member.save()
	return render(request, 'adm/adm_check.html', locals())

# 删除用户
def delete(request):
	if request.method == "POST":
		data = request.POST
		d_id = data.get("d_id")
		d_type = data.get("d_type")
		if d_type == "0":
			hunter = Hunter.objects.filter(id=int(d_id),type=d_type).first()
			hunter.delete()
			result = {"code": 10000, "msg": "删除成功"}
		elif d_type == "1":
			boss = Boss.objects.filter(id=int(d_id), type=d_type).first()
			boss.delete()
			result = {"code": 10000, "msg": "删除成功"}
		result = result
	return JsonResponse(result)

# 职位管理
def job_manage(request,status,page):
	"""

	:param request:
	:param status:0，1，2，3，4
	:param page:页数
	:return:待审核，审核中，已发布，审核未通过，已删除
	"""
	user = get_user(request)
	page = int(page)
	# 根据状态选取数据
	if status == "0":
		# 待审核
		job_obj = Job.objects.filter(check_status=0).order_by("time")
	elif status == "1":
		## 审核中
		job_obj = Job.objects.filter(check_status=1).all()
	elif status == "2":
		## 已发布
		job_obj = Job.objects.filter(check_status=2).all()
	elif status == "3":
		## 审核未通过
		job_obj = Job.objects.filter(check_status=3).all()
	elif status == "4":
		## 已删除
		job_obj = Job.objects.filter(check_status=4).all()
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
	return render(request,'adm/review_list.html',locals())

