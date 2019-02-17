from django.shortcuts import render
from .models import LikeCount, LikeRecord
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse


def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, 'You have not logged in yet!')
    
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model = content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'Object Does Not Exist')


    if request.GET.get('is_like') == 'true':  # 要点赞
        like_record, is_created = LikeRecord.objects.get_or_create(content_type=content_type , object_id=object_id, user=user)
        if is_created: # 正常情况 未点赞过 进行点赞
            like_count, is_created = LikeCount.objects.get_or_create(content_type=content_type , object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else: # 非正常情况  已点赞过， 不能重复点赞
            return ErrorResponse(402, 'You have already liked it.')
    else:
        #要取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 正常情况 有点赞过 取消点赞
            like_record_obj = LikeRecord.objects.get(content_type=content_type , object_id=object_id, user=user)
            like_record_obj.delete()
            # 点赞总数-1
            like_count, is_created = LikeCount.objects.get_or_create(content_type=content_type , object_id=object_id)
            if not is_created: # 正常情况
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else: # 非正常情况 新创建的
                return ErrorResponse(404, 'data error')
        else: # 非正常情况 本来就没点赞 不能取消点赞
            return ErrorResponse(403, 'You have not liked it.')