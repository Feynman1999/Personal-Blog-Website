from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete = models.DO_NOTHING)
    object_id = models.PositiveIntegerField() # 对应其它表中该对象的主键值(id)
    content_object = GenericForeignKey('content_type', 'object_id') # 类似一种更普适的外键

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add = True)
    # 用户对象 发出过的评论
    user = models.ForeignKey(User, related_name = "comments", on_delete = models.DO_NOTHING)

    root = models.ForeignKey('self', related_name = "root_comment", null=True, on_delete=models.DO_NOTHING)
    # parent_id = models.IntegerField(default = 0) # 这样每一个评论是一颗树 根节点的parent_id = 0
    parent = models.ForeignKey('self', related_name = "parent_comment", null=True, on_delete=models.DO_NOTHING)
    # 用户对象所发出的评论  被哪些评论回复过
    reply_to = models.ForeignKey(User, related_name = "replies", null=True, on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']

    