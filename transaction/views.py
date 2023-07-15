from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View


from basket.models import Basket
from .models import Transaction


class CreateTransaction(LoginRequiredMixin, View):
    template_name = "transaction/create_transaction.html"
    

    def post(self, request, basket_id):
        basket = Basket.objects.get(pk=basket_id)

        transaction = Transaction.objects.filter(user=request.user, status=Transaction.PENDING).first()
        if basket.user == request.user:
            if transaction:
                lines = basket.lines.all()
                total = sum([line.product.price * line.quantity for line in lines])
                if total > 0:
                    transaction.amount = total
                    transaction.save()
                    return render(request, self.template_name, {"transaction": transaction})
            else:
                lines = basket.lines.all()
                total = sum([line.product.price * line.quantity for line in lines])
                if total > 0:
                    transaction = Transaction.objects.create(user=request.user, amount=total, status=Transaction.PENDING)
                    return render(request, self.template_name, {"transaction": transaction})    
        raise Http404
        
