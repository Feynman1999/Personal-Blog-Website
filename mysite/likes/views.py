from django.shortcuts import render
from .models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType

def like_change(request):
    # 获取数据
    user = request.user
    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    is_like = request.GET.get('is_like')

    if is_like == 'true':
        #要点赞
        like_record, is_created = LikeRecord.objects.get_or_create(content_type=content_type , object_id=object_id, user=user)
        if is_created:
            #未点赞过 进行点赞
            like_count, is_created = LikeCount.objects.get_or_create(content_type=content_type , object_id=object_id, user=user)
            like_count.liked_num += 1
            like_count.save()
        else:
            # 已点赞过， 不能重复点赞
            pass
    else:
        #要取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exist():
            # 正常情况 有点赞过 取消点赞
            like_record_obj = LikeRecord.objects.get(content_type=content_type , object_id=object_id, user=user)
            like_record_obj.delete()
            # 点赞总数-1
            
        else: