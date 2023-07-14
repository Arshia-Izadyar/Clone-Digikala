from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Avg, Q
from django_filters import FilterSet
from django_filters.views import FilterView


from .models import Product


class HomeFilter(FilterSet):
    class Meta:
        model = Product
        fields = {"title": ["contains"], "category": ["exact"]}
        

class ProductHomeView(FilterView):
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    filterset_class = HomeFilter
    template_name = "products/home.html"
    
    
    def get_queryset(self):
        qs = super().get_queryset()
        return (
            qs.prefetch_related("reviews")
            .annotate(avg_rate=Avg("reviews__rate"))
            .filter(Q(avg_rate__gt=3) & Q(is_active=True))
        )
