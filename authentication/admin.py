from authentication.forms import UserChangeForm, UserCreationForm
from authentication.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ("username", "is_staff")
    list_filter = ("username", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Permissions", {"fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "is_staff"),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)


admin.site.register(User, UserAdmin)
