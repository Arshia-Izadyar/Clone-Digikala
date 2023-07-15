from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ShippingForm


class CreateShipping(LoginRequiredMixin, FormView):
    form_class = ShippingForm
    template_name = "shipping/add_shipping.html"
    success_url = '/'
    
    def form_valid(self, form):
        shipping = form.save(commit=False)
        shipping.user = self.request.user
        shipping.save()
    