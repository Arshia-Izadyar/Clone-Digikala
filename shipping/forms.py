from django import forms

from .models import Shipping
from accounts.models import UserAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ("sending_date", "delivery_method", "user_address")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ShippingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["user_address"].queryset = UserAddress.objects.filter(user=user)