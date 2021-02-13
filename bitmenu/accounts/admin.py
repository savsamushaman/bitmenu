from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterUserFormAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = RegisterUserFormAdmin
    ordering = ('id', 'email')

    add_fieldsets = (
        ("User Data", {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'email',
            ),
        }),
        ('User Privileges', {'classes': ('wide'),
                             'fields': ('is_superuser', 'is_staff', 'is_active')})
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Additional data",
            {
                'fields': (
                    'slug',
                )
            }

        )
    )
    list_display = ('username', 'id', 'email', 'is_staff')
    search_fields = ('username__contains', 'email__contains',)


admin.site.register(CustomUser, CustomUserAdmin)
