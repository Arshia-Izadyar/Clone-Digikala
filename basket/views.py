from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Basket
from .forms import AddToBasketForm, RemoveFromBasketForm


class AddToBasket(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(request.POST.get("next", "/"))
        basket_id = request.COOKIES.get("basket_id", None)
        basket = Basket.get_basket(basket_id)
        if basket is None:
            raise Http404

        response.set_cookie("basket_id", basket.id)

        if not basket.user_validate(request.user):
            raise Http404

        form = AddToBasketForm(request.POST or None)

        if form.is_valid():
            form.save_basket(basket)
        else:
            form_errors = form.errors.as_text()
            # You can log the form errors or handle them in a way that suits your application
            print(form_errors)
        return response


class RemoveFromBasket(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        response = HttpResponseRedirect(request.POST.get("next", "/"))

        basket_id = request.COOKIES.get("basket_id", None)
        basket = Basket.get_basket(basket_id=basket_id)
        if basket is None:
            raise Http404
        response.set_cookie("basket_id", basket.id)

        if not basket.user_validate(request.user):
            raise Http404

        form = RemoveFromBasketForm(request.POST or None)

        if form.is_valid():
            form.save_basket(basket)
        else:
            raise Http404

        return response


class DeleteBasket(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Basket, user=self.request.user)
        obj.lines.all().delete()
        return redirect("product:home-page")


class ShowBasketView(LoginRequiredMixin, TemplateView):
    model = Basket
    template_name = "basket/user_basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self, "basket_object"):
            self.basket_object = Basket.objects.prefetch_related("lines").get(user=self.request.user)
        lines = self.basket_object.lines.all()
        context["total_sum"] = sum([line.product.price * line.quantity for line in lines])
        context["lines"] = lines
        context["basket"] = self.basket_object
        return context
