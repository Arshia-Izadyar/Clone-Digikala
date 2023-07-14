from django.urls import path

from .views import ProductHomeView, ProductDetailView, AddReviewView

app_name = 'product'

urlpatterns = [
    path('', ProductHomeView.as_view(), name='home-page'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/add-review', AddReviewView.as_view(), name='review'),
    
    
]
