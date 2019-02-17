from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()

@register.filter
def get_comment_count(obj): # 此方法可能比views中处理较慢 但影响不大
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type = content_type, object_id = obj.pk).count()


@register.filter
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type':content_type.model, 
                                'object_id':obj.pk,
                                'reply_comment_id':0})
    return form


@register.filter
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type = content_type, 
                                    object_id = obj.pk, parent=None)
    return comments.order_by('-comment_time')