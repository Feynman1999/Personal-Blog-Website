import threading
import time

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import AC_detail
from django.http import JsonResponse
from django.core.cache import cache  # cache.clear()

from . import aoj


class Get_Spider(threading.Thread):
    def __init__(self, contest_id):
        self.contest_id = contest_id
        threading.Thread.__init__(self)
    
    def add_data(self):
        last_id = cache.get('AC_detail_last_id')
        if last_id is None:
            last_id = 0
        Dict = aoj.spider(last_id, self.contest_id)
        if Dict is None:
            print("没有新的数据！")
            return 
        n = len(Dict["id"])
        for i in range(n):
            ac_obj_num = AC_detail.objects.filter(name = Dict["name"][i], problem_id=ord(Dict["problem"][i])-ord('A')+1).count()
            if ac_obj_num == 0:
                AC_detail.objects.create(name = Dict["name"][i], problem_id=ord(Dict["problem"][i])-ord('A')+1, aoj_id = Dict["id"][i])
            
            if i == n-1:
                cache.set('AC_detail_last_id', Dict["id"][i], 3600*24)
        return 

    def run(self):
        cache.set('get_spider_running', 1 , 3600*24)
        try:
            self.add_data()
        except:
            print("运行爬虫时出错!")
        cache.set('get_spider_running', 0, 3600*24)


def add_match_timestamp(Dict):
    cpc_start_time = '2019-03-24 13:00:00'
    timeArray = time.strptime(cpc_start_time, "%Y-%m-%d %H:%M:%S")
    Dict['cpc_start_timestamp'] = int(time.mktime(timeArray)*1000) # 转为ms
    cpc_end_time = '2019-03-24 18:00:00'
    timeArray = time.strptime(cpc_end_time, "%Y-%m-%d %H:%M:%S")
    Dict['cpc_end_timestamp'] = int(time.mktime(timeArray)*1000) # 转为ms
    Dict['now_timestamp'] = int(time.time()*1000)
    if Dict['now_timestamp'] < Dict['cpc_start_timestamp']:
        Dict['timestamp_for_js'] = Dict['cpc_start_timestamp']
    elif Dict['now_timestamp'] < Dict['cpc_end_timestamp']:
        Dict['timestamp_for_js'] = Dict['cpc_end_timestamp']
    else:
        pass


def balloon_board(request):
    running_flag = cache.get('get_spider_running')
    if running_flag is None or running_flag == 0:
        get_spider = Get_Spider(134)
        get_spider.start() # 开启线程
        print("开始调用爬虫...")
    else:
        print("已经有爬虫在运行了")
    Dict = {}
    ac_0 = AC_detail.objects.filter(status=0)
    for item in ac_0: # 状态置为1
        item.status = 1
        item.save()
    ac_1 = AC_detail.objects.filter(status=1).order_by('id') # 已显示但还未处理
    ac_2 = AC_detail.objects.filter(status=2).order_by('-id') # 正在处理
    ac_3 = list(AC_detail.objects.filter(status=3).order_by('-id')) # 已经处理
    ac_3_up = 100
    if len(ac_3) > ac_3_up:
        ac_3 = ac_3[0:ac_3_up]
    Dict['ac_1'] = ac_1
    Dict['ac_2'] = ac_2
    Dict['ac_3'] = ac_3
    Dict['ac_3_up'] = ac_3_up
    Dict['workers'] = User.objects.filter(groups__name='2019ahucpc')
    add_match_timestamp(Dict)
    return render(request,'balloon/balloon.html', Dict)


def SuccessResponse(data):
    data['status'] = 'SUCCESS'
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def change_status(request):
    ac_id = request.GET.get('ac_id')
    source_status = request.GET.get('source_status')
    desti_status = request.GET.get('desti_status')
    deal_people = request.GET.get('deal_people')
    if int(source_status) == 1:
        deal_people = User.objects.get(username = deal_people)

    data={}
    ac_obj = AC_detail.objects.get(pk=ac_id)
    ac_obj.status = int(desti_status)
    if int(source_status) == 1:
        ac_obj.deal_people = deal_people
    ac_obj.save()

    data['student_id'] = ac_obj.student_id
    data['problem_id'] = ac_obj.get_problem()
    data['name'] = ac_obj.name
    data['deal_people'] = ac_obj.deal_people.username
    data['workers'] = [worker.username for worker in list(User.objects.filter(groups__name='2019ahucpc'))]
    return SuccessResponse(data)
