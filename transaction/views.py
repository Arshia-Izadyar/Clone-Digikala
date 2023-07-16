from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View


from basket.models import Basket
from .models import Transaction


class CreateTransaction(LoginRequiredMixin, View):
    template_name = "transaction/create_transaction.html"

    def get(self, request, basket_id):
        basket = Basket.objects.get(pk=basket_id)
        lines = basket.lines.all()
        total = sum([line.product.price * line.quantity for line in lines])

        transaction = Transaction.objects.filter(user=request.user, status=Transaction.PENDING).first()
        if basket.user == request.user:
            if transaction and total > 0:
                transaction.amount = total
                transaction.save()
                basket.lines.all().delete()
                return render(request, self.template_name, {"transaction": transaction, "lines": lines})
            else:
                if total > 0:
                    transaction = Transaction.objects.create(
                        user=request.user, amount=total, status=Transaction.PENDING, basket=basket
                    )
                    basket.lines.all().delete()
                    return render(request, self.template_name, {"transaction": transaction, "lines": lines})
        raise Http404


class GateWayConfirm(LoginRequiredMixin, View):
    # i dont have payment gateway so we skip the payment in gateway
    # we assume that the program claimed th transaction from gateway
    template_name = "transaction/confirm_transaction.html"

    def post(self, request, invoice_id):
        transaction = Transaction.objects.get(invoice_number=invoice_id)
        if request.user == transaction.user:
            transaction.status = 10
            transaction.save()
            # transaction.basket.delete()
        else:
            raise Http404

        return render(request, self.template_name, {"transaction": transaction})
