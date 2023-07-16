from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from shipping.models import ShippingItem
from django.utils.translation import gettext as _

User = get_user_model()


class Basket(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_baskets", null=True, blank=True
    )
    created_time = models.DateTimeField(_("Created Date"), auto_now_add=True)
    is_paid = models.BooleanField(_("Is paid"), default=False)

    def add_product(self, product, amount=1):
        line, created = self.lines.get_or_create(product=product, defaults={"quantity": int(amount)})
        if not created:
            line.quantity += int(amount)
            line.save()
        return line

    def remove_product(self, product):
        line, created = self.lines.get_or_create(product=product)
        if not created:
            line.quantity -= 1
        if line.quantity == 0:
            line.delete()
        else:
            line.save()

        return line

    def user_validate(self, user):      # Validate user that requested the basket 
        if user.is_authenticated:
            if self.user is not None and self.user != user:
                return False
            if self.user is None:
                self.user = user
                self.save()
        elif self.user is not None:
            return False
        return True

    @classmethod
    def get_basket(cls, basket_id):     # will retrive basket from id if no basket exists return None
        if basket_id is None:
            basket = cls.objects.create()
        else:
            try:
                basket = cls.objects.filter(pk=basket_id, is_paid=False).first()
            except cls.DoesNotExist:
                basket = None
        return basket

    def add_to_shipping(self, shipping):
        for line in self.lines.all():
            ShippingItem.objects.create(shipping=shipping, product=line.product, quantity=line.quantity)

    def __str__(self):
        return str(self.user)


class BasketLine(models.Model):     # products for basket added here
    quantity = models.PositiveSmallIntegerField(_("Quantity"), default=1)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name="lines")
    basket = models.ForeignKey(Basket, verbose_name=_("Basket"), on_delete=models.CASCADE, related_name="lines")
