from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = 'is_active',


admin.site.register(User, CustomUserAdmin)
# Register your models here.
