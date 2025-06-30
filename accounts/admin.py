from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Department


class UserAdmin(UserAdmin):
    model = User
    list_display = ("id","username", "role")
    list_filter = ("is_staff", "role")
    fieldsets = (
        ("Authenticate", {"fields": ("username", "password","role","department","is_staff")}),
        ("Group Permissions", {"fields": ("groups", "user_permissions")}),
        ("Last login", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username",)


admin.site.register(User, UserAdmin)
admin.site.register(Department) 
