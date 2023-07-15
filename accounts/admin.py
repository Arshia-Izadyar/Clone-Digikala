from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, UserAddress


# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
    
#     model = User
    
#     list_display = ('username', 'email', 'is_staff', 'is_active',)
#     list_filter = ('is_staff', 'is_active',)
    
#     search_fields = ('username', 'email',)
#     ordering = ('username',)
    
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active',
#          'is_superuser', 'groups', 'user_permissions')}),
#         ('Dates', {'fields': ('last_login', 'date_joined')})
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
#          ),
#     )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email', 'is_staff', 'is_active', 'phone_number')
    list_filter = ('is_staff', 'is_active',)

    search_fields = ('username', 'email',)
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    
    
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'address', 'city', 'state', 'zipcode')
    list_filter = ('user', 'city', 'state', 'zipcode')