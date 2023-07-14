from django.urls import path

from .views import ProductHomeView

urlpatterns = [
    path('', ProductHomeView.as_view(), name='home'),
]
