from django.db import models

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from product.models import Product
from lib.validators import validated_date
from accounts.models import UserAddress

User = get_user_model()

class Shipping(models.Model):
    DIGI_PLUS = 1
    DIGI_EXP = 2
    PROVIDER = 3
    methods = (
        (DIGI_PLUS, _("digikala plus")),
        (DIGI_EXP, _("digikala express")),
        (PROVIDER, _("Provider")),
        
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_shipping")
    sending_date = models.DateField(validators=[validated_date])
    delivery_method = models.PositiveSmallIntegerField(choices=methods, default=2)
    is_deliverd = models.BooleanField(default=False)
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name="shippings",  default=None)
    #TODO: add user address to db
    
    
    
    def __str__(self):
        return self.user.username
    
class ShippingItem(models.Model):
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)