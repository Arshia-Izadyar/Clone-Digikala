from django.urls import path

from .views import ProductHomeView, ProductDetailView, AddReviewView, CategoryListView, CategoryList

app_name = 'product'

urlpatterns = [
    path('', ProductHomeView.as_view(), name='home-page'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/add-review', AddReviewView.as_view(), name='review'),
    path('category/<slug:category>/', CategoryListView.as_view(), name='category'), # specific category views
    path('category/', CategoryList.as_view(), name='category-list'), # all categories in one page
    
    
]
