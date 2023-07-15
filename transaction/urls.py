from django.urls import path

from .views import CreateTransaction

app_name = "trans"

urlpatterns = [
    path('create/<int:basket_id>/', CreateTransaction.as_view(), name="create"),
]
