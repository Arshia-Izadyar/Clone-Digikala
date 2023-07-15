from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ShippingForm
from basket.models import Basket


class CreateShipping(LoginRequiredMixin, FormView):
    form_class = ShippingForm
    template_name = "shipping/add_shipping.html"

        
    def form_valid(self, form):
        shipping = form.save(commit=False)
        shipping.user = self.request.user
        shipping.save()
        basket_id = self.kwargs['basket_id']
        basket = Basket.get_basket(basket_id)
        basket.add_to_shipping(shipping)
        # basket.lines.all().delete()
        return redirect(reverse_lazy('transaction:create', kwargs={'basket_id': basket_id}))


