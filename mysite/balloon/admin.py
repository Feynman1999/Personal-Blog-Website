from django.contrib import admin
from .models import AC_detail


@admin.register(AC_detail)
class AC_detail_Admin(admin.ModelAdmin):
    list_display = ('status', 'student_id', 'name', 'problem_id', 'created_time', 'id')
    ordering = ('-created_time', ) # admin中类对象的显示顺序
