from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# 在用户的后台显示Profile
# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

# 继承
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'nickname' ,'email', 'is_active', 'is_staff', 'is_superuser')

    def nickname(self, obj):
        return obj.profile.nickname
        
    # 设置中文
    nickname.short_description = "昵称"

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id' ,'user', 'nickname')
    
    ordering = ('-id', ) # admin中类对象的显示顺序