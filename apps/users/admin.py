from django.contrib import admin

from .models import UserProfile, Email
# Register your models here.

admin.site.site_header = 'EVHarbor管理'
admin.site.site_title = 'EVHarbor站点管理'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'fullname', 'company', 'telephone', 'is_active')
    list_display_links = ('id', 'username')
    list_filter = ('date_joined',)
    search_fields = ('username', 'company')  # 搜索字段

    def fullname(self, obj):
        return obj.get_full_name()
    fullname.short_description = '姓名'

@admin.register(Email)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'send_time')
    list_display_links = ('id',)
    list_filter = ('send_time',)
    search_fields = ('receiver',)  # 搜索字段
