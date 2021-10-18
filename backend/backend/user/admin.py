from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

#https://realpython.com/customize-django-admin-python/

@admin.register(CustomUser)
class UserDisplay(admin.ModelAdmin):
    list_display= ('id', 'phone', 'email', 'username', 'profile_name', 'sex', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
    search_fields= ('email', 'phone')

