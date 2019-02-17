from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord

register = template.Library()

@register.filter
def get_like_count(obj): # 此方法可能比views中处理较慢 但影响不大
    content_type = ContentType.objects.get_for_model(obj)
    like_count_obj, created = LikeCount.objects.get_or_create(content_type = content_type, object_id = obj.pk)
    return like_count_obj.liked_num


@register.filter
def get_like_status(obj, user):
    # print(type(user))
    # print(user)
    content_type = ContentType.objects.get_for_model(obj)
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type, object_id = obj.pk, user=user).exists():
        return 'active'
    else:
        return ''


@register.filter
def get_content_type(obj): # 不用手写类型了
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model