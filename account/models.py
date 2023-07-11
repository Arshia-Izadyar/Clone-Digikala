from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField("Username", max_length=65, unique=True,
                                validators=[username_validator], error_messages="Username must be valid and unique")
    email = models.EmailField("Email address", unique=True)
    phone_number = models.CharField("Phone number", max_length=11, blank=True)
    first_name = models.CharField("First name", max_length=60)
    last_name = models.CharField("Last name", max_length=60)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField("Active", default=True)
    is_admin = models.BooleanField("Admin", default=False)
    is_staff = models.BooleanField("Staff", default=False)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
