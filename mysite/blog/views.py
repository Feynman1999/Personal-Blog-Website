from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from .models import Article, ArticleType
from read_count.utils import read_count_once
# from django.db.models import Count # 用于按类计数
import time


def make_pagination(request, articles_all):
    paginator = Paginator(articles_all, settings.NUM_IN_ONE_PAGE)
    page_of_articles = paginator.get_page(request.GET.get("page", 1))
    page_id_now = page_of_articles.number
    page_range = [ i for i in range(page_id_now-settings.PAGE_GAP,page_id_now+settings.PAGE_GAP+1)]
    if settings.PAGE_GAP*2+1 > page_of_articles.paginator.num_pages: # 如果页很少 就显示这些页
        page_range = [i for i in range(1, page_of_articles.paginator.num_pages+1)]
    elif page_range[0] < 1: #否则若前面超界 
        page_range = [i for i in range(1, 2*settings.PAGE_GAP+1+1)]
    elif page_range[-1] > page_of_articles.paginator.num_pages: #否则若后面超界 
        page_range = [i for i in range(page_of_articles.paginator.num_pages-2*settings.PAGE_GAP, page_of_articles.paginator.num_pages+1)]
    return page_range, page_of_articles


def init_dict(request, articles_all):
    Dict = {}
    # 统计每个类别有多少篇文章
    article_types = ArticleType.objects.all()
    article_types_list=[]
    for article_type in article_types:
        article_type.article_count = Article.objects.filter(article_type=article_type, is_deleted=False).count() # 直接加入新的属性
        article_types_list.append(article_type)
    # 统计每个归档日期有多少篇文章
    article_dates = Article.objects.filter(is_deleted = False).dates('created_time', 'month', order="DESC") # 返回一个列表   存在的桶！
    article_dates_dict = {} # 经测试 保持降序不变
    for article_date in article_dates:
        article_dates_dict[article_date]=Article.objects.filter(is_deleted=False, 
                                                                created_time__year=article_date.year,
                                                                created_time__month=article_date.month).count()
    Dict['article_types'] = article_types_list
    # Dict['article_types'] = ArticleType.objects.annotate(article_count=Count('article')) # article 是 models中Article的小写   problem: don't down how to add the filter : deleted=false 
    Dict['article_dates'] = article_dates_dict # 是一个字典 所以在模板中要用.items了
    Dict['page_range'], Dict['page_of_articles'] = make_pagination(request, articles_all) # 要显示的页码
    return Dict


def article_list(request):
    articles_all = Article.objects.filter(is_deleted = False)
    Dict = init_dict(request, articles_all)
    return render(request, "blog/article_list.html", Dict)

def article_list_with_type(request, type_id):
    article_type = get_object_or_404(ArticleType, pk=type_id)
    articles_all = Article.objects.filter(article_type=article_type, is_deleted = False)
    Dict = init_dict(request, articles_all)
    Dict['article_type'] = article_type
    return render(request, "blog/article_list_with_type.html", Dict)

def article_list_with_date(request, year, month):
    articles_all = Article.objects.filter(created_time__year=year, created_time__month=month, is_deleted = False)
    Dict = init_dict(request, articles_all)
    Dict['article_date'] = [year, month]
    return render(request, "blog/article_list_with_date.html", Dict)

def article_detail(request, article_id):

    article = get_object_or_404(Article, pk = article_id) # 若为md模式 则默认是md源码

    # 更新或创建关联的阅读计数
    read_cookie_key = read_count_once(request, article)

    Dict = {}
    Dict['article'] = article
    Dict['previous_article'] = Article.objects.filter(created_time__gt=article.created_time, is_deleted = False).last()
    Dict['next_article'] = Article.objects.filter(created_time__lt=article.created_time, is_deleted = False).first()
    response = render(request, "blog/article_detail.html", Dict)
    response.set_cookie(read_cookie_key, 'true', max_age=100) # cookie 100s后失效 for 阅读计数
    return response