import threading

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


# 考虑多线程 复杂方案：Celery  可定时执行一些任务
class Send_Email(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, 
                  '', 
                  settings.EMAIL_HOST_USER, 
                  [self.email], 
                  fail_silently = self.fail_silently,
                  html_message = self.text
        )


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField() # 对应其它表中该对象的主键值(id)
    content_object = GenericForeignKey('content_type', 'object_id') # 类似一种更普适的外键

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add = True)
    # 用户对象 发出过的评论       级联删除  删除用户时会删除相关联的评论
    user = models.ForeignKey(User, related_name = "comments", on_delete = models.CASCADE)

    root = models.ForeignKey('self', related_name = "root_comment", null=True, on_delete=models.CASCADE)
    # parent_id = models.IntegerField(default = 0) # 这样每一个评论是一颗树 根节点的parent_id = 0
    parent = models.ForeignKey('self', related_name = "parent_comment", null=True, on_delete=models.CASCADE)
    # 用户对象所发出的评论  被哪些评论回复过
    reply_to = models.ForeignKey(User, related_name = "replies", null=True, on_delete=models.CASCADE)


    def send_email(self):
        # 发送邮件通知       
        if self.parent is None:
            # 发给博客的作者
            email = self.content_object.get_email()
            subject = '有人评论你的博客(#^.^#) from RW\'s Blog' 
        else:
            # 发给评论的对象
            email = self.reply_to.email
            subject = '有人回复你的评论(#^.^#) from RW\'s Blog'

        if email != "":
            Dict = {}
            Dict['comment_text'] = self.text[0:100]
            Dict['url'] = self.content_object.get_url()+"#comment_id_"+str(self.pk)
            text = render_to_string('comment/email_tem.html', Dict)
            # import pdb # 设置断点
            # pdb.set_trace()
            send_email = Send_Email(subject, text, email)
            send_email.start() # 开启线程

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']

    