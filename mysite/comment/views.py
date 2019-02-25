from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.conf import settings

from .models import Comment
from .forms import CommentForm
from blog.templatetags.md2html import md2html_1
from likes.templatetags.likes_tags import *



def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        Comment_obj = Comment()
        Comment_obj.user = request.user
        Comment_obj.text = comment_form.cleaned_data['text']
        Comment_obj.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:  # 不是直接回复文章的  
            Comment_obj.root = parent.root if not parent.root is None else parent
            Comment_obj.parent = parent
            Comment_obj.reply_to = parent.user
        Comment_obj.save()
        # return redirect(referer)

        # 邮件通知
        if settings.EMAIL_COMMENT_SEND:
            Comment_obj.send_email()

        data['status'] = 'SUCCESS'
        data['username'] = request.user.username
        data['comment_time'] = localtime(Comment_obj.comment_time).strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = md2html_1(Comment_obj.text)
        data['content_type'] = get_content_type(Comment_obj) # ajax增加评论点赞用
        if not parent is None: # 不是直接回复文章的
            data['reply_to_username'] = Comment_obj.reply_to.username
            data['root_pk'] = Comment_obj.root.pk
            data['parent_id'] = Comment_obj.parent.pk
        else:
            data['reply_to'] = None
        data['pk'] = Comment_obj.pk
    else:
        # return render(request, 'error.html', {'message': comment_form.errors.as_text(), 'redirect_to': referer})
        data['message'] = list(comment_form.errors.values())[0][0]
        data['status'] = 'ERROR'
    return JsonResponse(data)
