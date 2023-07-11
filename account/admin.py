# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
# from .models import User
#
#
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = [
#         "email",
#         "username",
#         "is_staff",
#     ]
#     fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number",)}),)
#     add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("phone_number",)}),)
