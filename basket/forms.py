from django import forms
from product.models import Product
from .models import BasketLine


class AddToBasketForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects, widget=forms.HiddenInput())
    quantity = forms.IntegerField(initial=1)

    def save_basket(self, basket):
        product = self.cleaned_data["product"]
        quantity = self.cleaned_data["quantity"]
        basket.add_product(product=product, amount=quantity)
        return basket


class RemoveFromBasketForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())

    def save_basket(self, basket):
        product = self.cleaned_data["product"]
        basket.remove_product(product=product)
        return basket
