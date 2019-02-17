from django.contrib import admin
from .models import LikeCount, LikeRecord


@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'content_object', 'liked_num')
    ordering = ('object_id', )


@admin.register(LikeRecord)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'liked_time')
    ordering = ('-liked_time', )