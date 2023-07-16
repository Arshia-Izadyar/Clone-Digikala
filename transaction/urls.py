from django.urls import path

from .views import CreateTransaction, GateWayConfirm

app_name = "transaction"

urlpatterns = [
    path("create/<int:basket_id>/", CreateTransaction.as_view(), name="create"),
    path("confirm/<uuid:invoice_id>/", GateWayConfirm.as_view(), name="confirm"),
]
