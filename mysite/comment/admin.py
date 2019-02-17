from django.contrib import admin
from .models import Comment

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id' ,'parent', 'root', 'content_object', 'text', 'comment_time', 'user')
    
    ordering = ('-comment_time', ) # admin中类对象的显示顺序