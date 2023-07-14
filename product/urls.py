from django.urls import path

from .views import ProductHomeView

urlpatterns = [
    path('home/', ProductHomeView.as_view(), name='home'),
]
