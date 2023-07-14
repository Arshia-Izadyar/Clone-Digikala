from django.shortcuts import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.db.models import Avg, Q
from django_filters import FilterSet
from django_filters.views import FilterView
from django.contrib.auth.decorators import  login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render


from .models import Product, Category
from .forms import AddReviewForm


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


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    queryset = Product.objects.prefetch_related("reviews").annotate(avg_rate=Avg("reviews__rate"))
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        product = context['product']
        context["reviews"] = product.reviews.all()
        context["avg_rate"] = product.avg_rate
        context["add_review_form"] = AddReviewForm()
        return context
    
class AddReviewView(DetailView):
    model = Product
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = AddReviewForm(request.POST)
        obj = self.get_object()
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = obj
            review.is_validated = True
            review.save()
        return HttpResponseRedirect(obj.get_absolute_url())
    



class CategoryFilter(FilterSet):
    class Meta:
        model = Product
        fields = {"title": ["contains"], "provider": ["exact"], "is_active":  ["exact"]}


class CategoryListView(FilterView):
    filterset_class = CategoryFilter
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    template_name = "products/category.html"
    
    def get_queryset(self):
        slug = self.kwargs["category"]
        return Product.objects.filter(category__slug=slug).annotate(avg_rate=Avg("reviews__rate")).order_by("title")
    
    
class CategoryList(ListView):   # just to show the list of categories in one page for the user
    template_name = "products/category_list.html"
    context_object_name = "categories"
    queryset = Category.objects.all()

