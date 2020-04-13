import hashlib, smtplib, random
from django.shortcuts import render
from email.mime.text import MIMEText
from Admins.models import *
from Graduate.models import *
from Boss.models import *
from django.http import HttpResponseRedirect


## 密码加密
def setPassword(password):
	## 实现一个密码加密
	md5 = hashlib.md5()  ## 创建一个md5的实例对象
	md5.update(password.encode())  ## 进行加密
	result = md5.hexdigest()
	return result


# 注册
def register(request):
	if request.method == "POST":
		email = request.POST.get('email')
		password = request.POST.get("password")
		password2 = request.POST.get("password2")
		type = request.POST.get("type")
		# 判断是否选择身份
		if type:
			if email:
				if password and password2:
					if password2 == password:
						if type == "0":
							LoginUser = Hunter.objects.filter(type=type, email=email).first()
							if not LoginUser:
								user = Hunter()
								user.email = email
								user.name = email
								user.type = type
								user.password = setPassword(password)
								user.save()
								response = HttpResponseRedirect('/login/')
								return response
							else:
								error_msg = '邮箱已经被注册，请登录'
						elif type == "1":
							LoginUser = Boss.objects.filter(type=type, email=email).first()
							if not LoginUser:
								user = Boss()
								user.email = email
								user.name = email
								user.type = type
								user.password = setPassword(password)
								user.save()
								response = HttpResponseRedirect('/login/')
								return response
							else:
								error_msg = '邮箱已经被注册，请登录'
						elif type == "2":
							LoginUser = Admins.objects.filter(type=type, email=email).first()
							if not LoginUser:
								user = Admins()
								user.email = email
								user.name = email
								user.type = type
								user.password = setPassword(password)
								user.save()
								response = HttpResponseRedirect('/login/')
								return response
							else:
								error_msg = '邮箱已经被注册，请登录'
					else:
						error_msg = '密码不一致，请重新输入'
				else:
					error_msg = '密码不可以为空'
			else:
				error_msg = '邮箱不可以为空'
		else:
			error_msg = '请选择身份'
	return render(request, 'register.html', locals())


# 登陆
def login(request):
	if request.method == "POST":
		error_msg = ''
		email = request.POST.get("email")
		type = request.POST.get("type")
		password = request.POST.get("password")
		if type:
			if email:
				if type == "0":
					user = Hunter.objects.filter(type=type, email=email).first()
					if user:
						## 用户存在
						if user.password == setPassword(password):
							response = HttpResponseRedirect('/Graduate/index/')
							response.set_cookie("useremail", user.email)
							response.set_cookie("usertype", user.type)
							response.set_cookie("userid", user.id)
							request.session['useremail'] = user.email
							request.session['usertype'] = user.type
							return response
						else:
							error_msg = '密码错误'
					else:
						error_msg = '用户不存在'
				elif type == "1":
					user = Boss.objects.filter(type=type, email=email).first()
					if user:
						## 用户存在
						if user.password == setPassword(password):
							response = HttpResponseRedirect('/Boss/index/1')
							response.set_cookie("useremail", user.email)
							response.set_cookie("usertype", user.type)
							response.set_cookie("userid", user.id)
							request.session['useremail'] = user.email
							request.session['usertype'] = user.type
							return response
						else:
							error_msg = '密码错误'
					else:
						error_msg = '用户不存在'
				elif type == "2":
					user = Admins.objects.filter(type=type, email=email).first()
					if user:
						## 用户存在
						if user.password == setPassword(password):
							response = HttpResponseRedirect('/Admins/index/1')
							response.set_cookie("useremail", user.email)
							response.set_cookie("usertype", user.type)
							response.set_cookie("userid", user.id)
							request.session['useremail'] = user.email
							request.session['usertype'] = user.type
							return response
						else:
							error_msg = '密码错误'
					else:
						error_msg = '用户不存在'
			else:
				error_msg = '邮箱不可以为空'
		else:
			error_msg = '请选择你的身份'
	return render(request, "login.html", locals())


# 发送邮件
def send_email(email, content):
	subject = "毕业吧忘记密码服务"
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


# 忘记密码
def forget(request):
	# 获取type和邮箱，验证是否存在，存在直接发送密码
	if request.method == "POST":
		error_msg = ""
		email = request.POST.get("email")
		type = request.POST.get("type")
		if type:
			if email:
				if type == "0":
					user = Hunter.objects.filter(type=type, email=email).first()
					if user:
						# 获取密码发送邮件
						code = random.randint(100000, 999999)
						user.password = setPassword(str(code))
						content = "您的密码已修改为：%s" % (code)
						user.save()
						send_email(email, content)
						error_msg = "邮件已发送"
					else:
						error_msg = '用户不存在'
				elif type == "1":
					user = Boss.objects.filter(type=type, email=email).first()
					if user:
						# 获取密码发送邮件
						code = random.randint(100000, 999999)
						user.password = setPassword(str(code))
						content = "您的密码已修改为：%s" % (code)
						user.save()
						send_email(email, content)
						error_msg = "邮件已发送"
					else:
						error_msg = '用户不存在'
				elif type == "2":
					user = Admins.objects.filter(type=type, email=email).first()
					if user:
						# 获取密码发送邮件
						code = random.randint(100000, 999999)
						user.password = setPassword(str(code))
						content = "您的密码已修改为：%s" % (code)
						user.save()
						send_email(email, content)
						error_msg = "邮件已发送"
					else:
						error_msg = '用户不存在'
			else:
				error_msg = "邮箱不可为空"
		else:
			error_msg = "请选择身份"

	return render(request, "forget-password.html", locals())


# 主页
def index(request):
	return render(request, "index.html")
