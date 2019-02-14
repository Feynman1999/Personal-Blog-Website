from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse

from blog.models import Article
from read_count.utils import *
from .forms import *
import time

def index(request):
    return render(request, 'index.html')

def spe(request):
    return render(request, 'spe.html')

read_data_cache_gap = 60 # second
hot_data_cache_gap = 3600 # second

def statistics(request):

    ct = ContentType.objects.get_for_model(Article)
    read_data_list_1, read_data_list_2 = get_days_data(ct, 7, read_data_cache_gap)

    Dict = {}
    Dict['read_data_list_1'] = read_data_list_1
    Dict['read_data_list_2'] = read_data_list_2
    Dict['hot_data_today'] = get_hot_data_somedays(ct, 1, 7, hot_data_cache_gap) # 最多显示3篇文章
    Dict['hot_data_week'] = get_hot_data_somedays(ct, 7, 7, hot_data_cache_gap)
    Dict['hot_data_month'] = get_hot_data_somedays(ct, 30, 7, hot_data_cache_gap)
    Dict['read_data_cache_gap'] = read_data_cache_gap
    Dict['hot_data_cache_gap'] = hot_data_cache_gap
    return render(request, 'statistics.html', Dict)


def about(request):
    return render(request, 'about.html')


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
    return render(request, 'login.html', Dict)


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
    return render(request, 'register.html', Dict)