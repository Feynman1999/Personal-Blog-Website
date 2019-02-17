from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# from mdeditor.fields import MDTextField #必须导入
from read_count.models import ReadNum_interface, ReadDetail


class ArticleType(models.Model):
    type_name = models.CharField(max_length=60)
    def __str__(self):
        return self.type_name

class Article(models.Model, ReadNum_interface):
    title = models.CharField(max_length = 120)
    # content = RichTextUploadingField()
    content = RichTextUploadingField()
    article_type = models.ForeignKey(ArticleType, on_delete=models.CASCADE, default = 1) # 默认是pk为1的那个type  , related_name='article_article'
    created_time = models.DateTimeField(auto_now_add=True)    # create_time = models.DateTimeField(default=timezone.now)
    last_updated_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = 1) # 1是pk
    is_deleted = models.BooleanField(default = False) # 假删
    
    read_details = GenericRelation(ReadDetail) # 建立关系后 可由article_obj对应到多条readdetail_obj

    def __str__(self):  
        return "Article: {}".format(self.title) 

    class Meta:
        ordering = ['-created_time']  # 按照时间倒叙排列


