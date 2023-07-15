from django.db import models, transaction
from django.utils.translation import gettext as _
from django.db.models import Count, Sum, Q, DecimalField
from django.db.models.functions import Coalesce
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model

import uuid 

from basket.models import Basket
User = get_user_model()

    
class Transaction(models.Model):
    PAID = 10
    PENDING = 0
    NOT_PAID = -10
    
    transaction_status = (
        (PAID, _("paid")),
        (PENDING, _("pending")),
        (NOT_PAID, _("Not paid"))
    )
    
    CHARGE = 1
    PURCHASE = 2
    
    transaction_type = (
        (PURCHASE, _("Purchase")),
        (CHARGE, _("Charge"))
    )
    
    user = models.ForeignKey(User, verbose_name=_("User"), related_name="transactions", on_delete=models.SET("deleted_user"))
    amount = models.DecimalField(verbose_name=_("Amount"), max_digits=11, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=transaction_type, default=PURCHASE)
    status = models.PositiveSmallIntegerField(choices=transaction_status, default=NOT_PAID)
    created_date = models.DateTimeField(auto_now_add=True)
    invoice_number = models.UUIDField(max_length=140 , default=uuid.uuid4)
    basket = models.ForeignKey(Basket, related_name="transactions", on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.user.username} > {self.status} > {self.amount}"
    
    @classmethod
    def get_user_report(cls, usr):
        positive = Sum("transactions__amount", filter=Q(transactions__type=Transaction.CHARGE))
        negative = Sum("transactions__amount", filter=Q(transactions__type=Transaction.PURCHASE))
        total = User.objects.filter(username=usr).aggregate(
            sum=Coalesce(positive, 0, output_field=DecimalField()) - Coalesce(negative, 0, output_field=DecimalField())
        )
        return total["sum"]

    @classmethod
    def purchase(cls, usr, amount):
        if cls.get_user_report(usr) >= amount:
            return cls.objects.create(user=usr, transaction_type=2, amount=amount)
        else:
            raise ValidationError(f"cannot transfer {amount}")

            
    @classmethod
    def calc_score(cls, usr):
        with transaction.atomic():
            
            obj = User.objects.select_for_update().get(username=usr.username)
            total = User.objects.filter(username=usr.username).aggregate(
                total=Sum("transactions__amount", filter=Q(transactions__type=Transaction.PURCHASE))
            )['total']
           
            if total is None:
                score = 0
            else:
                score = (total / 10) * 5
            obj.score = score
           
            obj.save() 
            
                
            
class Wallet(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Wallet"), related_name="wallet", on_delete=models.CASCADE)
    total = models.PositiveBigIntegerField(default=0)
    
    @classmethod
    def set_wallet(cls, user):
        with transaction.atomic():
            
            try:
                obj = cls.objects.select_for_update().get(user=user)
            except ObjectDoesNotExist:
                obj = cls.objects.create(user=user)
            total = Transaction.get_user_report(usr=user)
            if total is not None:
                obj.total = total
            else:
                obj.total = 0
            obj.save()
    

