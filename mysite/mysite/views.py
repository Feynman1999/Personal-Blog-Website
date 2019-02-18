from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse

from blog.models import Article
from read_count.utils import *


def index(request):
    return render(request, 'index.html')


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


def spe(request):
    return render(request, 'spe.html')


def about(request):
    return render(request, 'about.html')
