from django.urls import path

from .views import CreateShipping

app_name = "shipping"

urlpatterns = [
    path('<int:basket_id>/', CreateShipping.as_view(), name="create")
]
