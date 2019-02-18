from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

from read_count.utils import *
from .forms import *


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