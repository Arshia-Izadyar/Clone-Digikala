from django.urls import path, include

from .views import ShowBasketView, AddToBasket, RemoveFromBasket

app_name = "basket"

urlpatterns = [
    path("", ShowBasketView.as_view(), name="basket"),
    path("add/", AddToBasket.as_view(), name="add"),
    path("remove/", RemoveFromBasket.as_view(), name="remove"),
    
]
