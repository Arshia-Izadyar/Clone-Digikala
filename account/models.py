from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


from .managers import CustomUserManager

class User(AbstractUser):
    CONSUMER = 1
    PROVIDER = 2
    user_type = (
        (CONSUMER, "Consumer"),
        (PROVIDER, "Provider"),
    )
    
    
    email = models.EmailField(_("E-mail"), unique=True)
    phone_number = models.CharField(_("Phone number "), max_length=12, unique=True)
    is_admin = models.BooleanField(_("Admin status"), default=False) 
    user_score = models.PositiveIntegerField(_("User score"), default=0)
    user_type = models.PositiveSmallIntegerField(_("User type"), choices=user_type, default=CONSUMER)
    
    
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
        ),
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "phone_number")
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_address")
    title = models.CharField(_("Title"), max_length=40)
    zipcode = models.CharField(_("Zip code"), max_length=10)
    address = models.TextField(_("Address"))
    decription = models.TextField(_("Description"))
    
    def __str__(self):
        return f" {self.title} > {self.zipcode} > {self.user.username}"
    
    
    