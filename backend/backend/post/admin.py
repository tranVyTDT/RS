from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post

#https://realpython.com/customize-django-admin-python/

@admin.register(Post)
class UserDisplay(admin.ModelAdmin):
    list_display= ('post_id', 'title', 'is_approve_staff', 'is_approve_director')
    search_fields= ('post_id', 'title')
