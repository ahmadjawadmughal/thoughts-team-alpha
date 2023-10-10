from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User,UserProfile
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id","first_name", "last_name","username", "email" ]
    search_fields = ("username",)


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "date_of_birth"]



