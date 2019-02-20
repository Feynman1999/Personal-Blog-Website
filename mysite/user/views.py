import string, random, time

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail

from read_count.utils import *
from .forms import *
from .models import Profile


# 页面登陆
def login(request):
    if request.method == 'POST' :
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = LoginForm()

    Dict = {}
    Dict['login_form'] = login_form
    return render(request, 'user/login.html', Dict)


# modal登陆 (using ajax)
def login_for_modal(request):
    if request.method == 'POST' :
        login_form = LoginForm(request.POST)
        data = {}
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
        return JsonResponse(data)
    else:
        pass


def register(request):
    if request.method == 'POST' :
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()   # user = User()       user.username = username   user.email = email  user.set_password(password) 
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        reg_form = RegForm()

    Dict = {}
    Dict['reg_form'] = reg_form
    return render(request, 'user/register.html', Dict)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('index')))


def user_info(request):
    Dict = {}
    return render(request, 'user/user_info.html', Dict)


def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('index'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile_obj, is_created = Profile.objects.get_or_create(user=request.user)
            profile_obj.nickname = nickname_new
            profile_obj.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    
    Dict = {}
    Dict['form'] = form
    Dict['page_title'] = '修改昵称'
    Dict['form_title'] = '修改昵称'
    Dict['submit_text'] = '修改'
    Dict['return_back_url'] = redirect_to
    return render(request, 'user/form_for_change.html', Dict)


def bind_email(request):
    redirect_to = request.GET.get('from', reverse('index'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
        else:
            pass
    else:
        form = BindEmailForm()
    
    Dict = {}
    Dict['form'] = form
    Dict['page_title'] = '绑定邮箱'
    Dict['form_title'] = '绑定邮箱( 注意：当前页面刷新后需要重新发送验证码)'
    Dict['submit_text'] = '绑定'
    Dict['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', Dict)


def make_verification_code():
    return ''.join(random.sample(string.ascii_letters+string.digits, 4))


def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != "":
        code = make_verification_code()
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'error! 发送太频繁，需间隔1分钟发送！'
        else:   
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = int(time.time())
            # 发送邮件
            send_mail(
                '绑定邮箱 from [RandomWalker\'s Blog]♪(･ω･)ﾉ',
                '您的验证码为：{}'.format(code),
                '763972750@qq.com',
                [email],
                fail_silently=False  # 不忽略错误
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'error! 邮件地址不能为空!'

    return JsonResponse(data)