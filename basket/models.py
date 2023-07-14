from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_baskets", null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

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

    def user_validate(self, user):
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
    def get_basket(cls, basket_id):
        if basket_id is None:
            basket = cls.objects.create()
        else:
            try:
                basket = cls.objects.filter(pk=basket_id).first()
            except cls.DoesNotExist:
                basket = None
        return basket

    def __str__(self):
        return str(self.user)


class BasketLine(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="lines")
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="lines")