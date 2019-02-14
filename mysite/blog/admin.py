from django.contrib import admin
from .models import Article, ArticleType


# Register your models here.

@admin.register(ArticleType)
class ArticleType_Admin(admin.ModelAdmin):
    list_display = ('id', 'type_name')



@admin.register(Article)
class Article_Admin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'article_type', 'get_read_num', 'is_deleted', 'created_time', 'last_updated_time')
    ordering = ('-created_time', ) # admin中类对象的显示顺序

#admin.site.register(Article, Article_Admin)

