
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("product.urls")),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include('allauth.urls')),
    path("basket/", include("basket.urls")),
    path('transaction/', include("transaction.urls"))


]
