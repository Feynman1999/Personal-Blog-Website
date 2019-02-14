import datetime
from django.db.models.fields import exceptions
from django.db.models import Sum
from django.core.cache import cache  # cache.clear()
from django.contrib.contenttypes.models import ContentType
from read_count.models import ReadNum, ReadDetail
from blog.models import Article
from django.utils import timezone


def read_count_once(request, obj):
    ct = ContentType.objects.get_for_model(obj) 
    key = "{}_{}_read".format(ct.model, obj.pk)

    if not request.COOKIES.get(key): # 需要更新计数辣
        # 一篇文章的总阅读数加1
        ReadNum_obj, flag = ReadNum.objects.get_or_create(content_type = ct, object_id = obj.pk) # 默认read_num=0
        ReadNum_obj.read_num += 1  # 计数加1
        ReadNum_obj.save()

        # 一篇文章对应当天的阅读数加1
        ReadDetail_obj, flag = ReadDetail.objects.get_or_create(content_type = ct, object_id = obj.pk, date=timezone.now().date())
        ReadDetail_obj.read_num += 1  # 计数加1
        ReadDetail_obj.save()

    return key


# 过去一段时间内的总访问量
def get_days_data(content_type, day_length, cache_timegap = 60):
    ans1 = cache.get('read_data_1_'+str(day_length))
    if ans1 is None:
        today = timezone.now().date()
        data_list_1 = []
        date_list_2 = []
        for i in range(day_length-1, -1, -1): # 包括今天  共day_length天
            date = today - datetime.timedelta(days = i)
            date_list_2.append(date.strftime('%m/%d'))
            read_details = ReadDetail.objects.filter(content_type=content_type, date=date) # 多个对象 
            result = read_details.aggregate(read_num_sum = Sum('read_num')) # 返回一个字典
            data_list_1.append(result['read_num_sum'] or 0) # none 时 为 0
        cache.set('read_data_1_'+str(day_length), data_list_1, cache_timegap)
        cache.set('read_data_2_'+str(day_length), date_list_2, cache_timegap)
        return data_list_1, date_list_2
    return ans1, cache.get('read_data_2_'+str(day_length))


# # 今天(截至现在)最火热的文章
# def get_hot_data_today(content_type, limit_num):
#     today = timezone.now().date()
#     read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
#     return read_details[0:limit_num]

# # 昨天最火热的文章
# def get_hot_data_yesterday(content_type, limit_num):
#     today = timezone.now().date()
#     yesterday = today - datetime.timedelta(days=1)
#     read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
#     return read_details[0:limit_num]


# 过去一段时间最火热的文章 (包括今天) 
# 加入缓存
def get_hot_data_somedays(content_type, day_length, limit_num, cache_timegap = 3600): # 同一篇博客要分组 加和计算
    ans = cache.get('hot_data_'+str(day_length))
    if ans is None:
        today = timezone.now().date()
        date = today - datetime.timedelta(days=day_length-1)
        articles = Article.objects.filter(read_details__date__lte = today, 
                                        read_details__date__gte = date) \
                                        .values('id', 'title') \
                                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                                        .order_by('-read_num_sum')
        cache.set('hot_data_'+str(day_length), articles[:limit_num], cache_timegap)
        return articles[:limit_num]
    return ans





