from django.urls import path

from .views import ProductHomeView

app_name = 'product'

urlpatterns = [
    path('home/', ProductHomeView.as_view(), name='home-page'),
]
