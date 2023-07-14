from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User, UserAddress


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('phone_number', 'email',)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone_number', 'email',)


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ("title", "zipcode", "city", "state", "address", "decription")
    