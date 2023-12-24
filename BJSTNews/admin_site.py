"""
@ author: neo
@ date: 2023-12-15  12:48 
@ file_name: admin_site.PY
@ github: https://github.com/Underson888/
"""
from django.contrib import admin
# Register your models here.
from BJSTArticle.models import Topic, Entry
from django.contrib.admin import AdminSite
from BJSTAccount.models import BJSTAccount
from BJSTAccount.admin import BJSTAccountAdmin
from BJSTComments.models import Comment

class BJSTNewsAdminSite(AdminSite):
    site_header = '巴基斯坦小站管理界面'
    site_title = '巴基斯坦小站管理'

    def __init__(self, name='admin'):
        super().__init__(name)

    def has_permission(self, request):
        return request.user.is_superuser


admin_site = BJSTNewsAdminSite(name='admin')

admin_site.register(BJSTAccount, BJSTAccountAdmin)
admin_site.register(Topic)
admin_site.register(Entry)
admin_site.register(Comment)
