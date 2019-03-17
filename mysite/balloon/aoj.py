# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import json
import random
import time


def login():
    url="http://ccpc.ahu.edu.cn/Login.aspx"
    data={
    "__VIEWSTATE": "/wEPDwUKMjA0OTI1OTkzN2RkfCO0R/wSKttR0DSJAdKJm/7JkHb0FAZxHfGNzIg/t9M=",
    "__VIEWSTATEGENERATOR": "C2EE9ABB",
    "__EVENTVALIDATION": "/wEdAAQ0Av07VjuDOILkZ2b1jVggNmJORucp1eQiHzMn79KmSwOmdXA3Nr9IYISzlILy1ebN+DvxnwFeFeJ9MIBWR693k5u+TsFuMU8EvT7og4gnu/Z55GQ9R3czfkLcqreeoqY =",
    "TUsername": "jzhou",
    "TPassword": "jzhou07037",
    "Button1": "登 录",
    }
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    session = requests.session()
    session.post(url,headers=header,data=data)
    return session
    #print(html.text)

def getstring(url):

    session=login()

    header=[
        {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)',
         },
        {'User-Agent':'Mozilla/4.04[en](Win95;I;Nav)'},
    ]
    res = session.get(url,headers = header[random.randint(0,1)])
    if res.text.find("页面禁止频繁刷新，你需要等待至少3秒才可以刷新页面！")!=-1:
        return ["#"]
    #print(res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    try:
        tmp=soup.find('table',{'class':'table table-striped'})
        tmp=tmp.find('script',{'type':'text/javascript'})
    except:
        return ["#"]
    string=tmp.get_text()
    string=string.split(';')
    string.pop()
    return string

def spider(lastid,contest_id):
    '''
    lastid: int类型
    该爬虫返回那些提交号严格大于lastid的AC提交信息
    :return:
    返回一个字典
    {
    "id":int_list,
    "name":string_list,
    "problem":string_list,
    }
    3个key对应的都是一个列表，里面存储的分别是提交号、姓名、过题的题号
    '''
    ids=[]
    names=[]
    problems=[]

    now=400000
    count=1
    while True:

        print("正在爬取第",count,"页......")
        flag=True
        url='http://ccpc.ahu.edu.cn/ContestStatus.aspx?cid='+str(contest_id)+"&to="+str(now)+"&pid=&un=&cp=&r=Accepted"
        #start=time.clock()
        string=getstring(url)
        if(len(string)==0):
            break
        if string[0]=="#":
            print("爬取到不正确的页面，正在尝试重新爬取......")
            sleep(3)
            continue
        for each in string:
            tmp=each
            tmp=tmp.split(',')
            #print(tmp)
            id=int(tmp[0].split('(')[1])
            name=tmp[1].replace("'","")
            problem=tmp[4].replace("'","")
            if id<=lastid:
                flag=False
            if id<=lastid:
                continue
            now=id
            #print(id,name,problem)
            ids.append(id)
            names.append(name)
            problems.append(problem)
        if flag==False:
            break
        now-=1
        #end=time.clock()
        #print("时间测试：",end-start)
        time.sleep(1)               # 1秒放刷QvQ
        count+=1
    print("爬取完毕！")
    ids.reverse()
    names.reverse()
    problems.reverse()
    if len(ids)==0:
        return None
    return {"id":ids,"name":names,"problem":problems}


# if __name__=='__main__':

    # tmp=spider(0,134)
    # n=len(tmp["id"])
    # for i in range(n):
    #     print(tmp["id"][i],'',tmp["name"][i],'',tmp["problem"][i])
