from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from lib.validators import validate_rate

User = get_user_model()

class IsActiveManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related("category", "brand")

    def active(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(is_active=True)

    def de_active(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).exclude(is_active=True)
    

class Category(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.title
    

class Provider(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    bio = models.TextField(_("Biography"), null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(_("Category"), Category, on_delete=models.PROTECT, related_name="categories")
    provider = models.ForeignKey(_("Provider"), Provider, on_delete=models.PROTECT, related_name="providers")
    
    title = models.CharField(_("Title"), max_length=50)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    description = models.TextField(_("Description"), null=True, blank=True)    
    is_active = models.BooleanField(_("Is Active"), default=True)
    
    image = models.ImageField(_("Image"), upload_to='./products', null=True, blank=True)
    
    objects = IsActiveManager()
    
    def __str__(self):
        return self.title + " - " + self.category.title + " - " + self.provider.name
    
    

class WishList(models.Model):
    user = models.ForeignKey(_("User"), User, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(_("Product"), Product, on_delete=models.CASCADE, related_name="wishlists")
    
    def __str__(self) -> str:
        return self.user.username + " - " + self.product.title

class Review(models.Model):
    user = models.ForeignKey(_("User"), User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(_("Product"), Product, on_delete=models.CASCADE, related_name="reviews")  
    
    comment = models.TextField(_("Comments") ,null=True)
    rate = models.IntegerField(_("Rate") ,validators=[validate_rate])
    
    def __str__(self):
        return self.user.username + " - " + self.product.title + " - " + str(self.rate)
    
    class Meta:
        unique_together = ["user", "product"]