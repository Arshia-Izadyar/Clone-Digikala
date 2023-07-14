from django import forms

from .models import Review, WishList

class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', 'rate')
        
        
class AddWishListForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = []