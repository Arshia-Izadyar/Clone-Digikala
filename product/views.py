from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views import View
from django.db.models import Avg, Q
from django_filters import FilterSet
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy


from .models import Product, Category, WishList
from .forms import AddReviewForm, AddWishListForm
from basket.forms import AddToBasketForm


# home view for products and detail view


class HomeFilter(FilterSet):
    class Meta:
        model = Product
        fields = {"title": ["contains"], "category": ["exact"]}


class ProductHomeView(FilterView):
    model = Product
    context_object_name = "products"
    paginate_by = 10
    filterset_class = HomeFilter
    template_name = "products/home.html"
    
    @method_decorator(cache_page(60 * 1))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        product = context["product"]
        context["reviews"] = product.reviews.all()
        context["avg_rate"] = product.avg_rate
        context["add_review_form"] = AddReviewForm()
        context["add_to_basket"] = AddToBasketForm({"product": product.id, "quantity": 1})
        return context


# review and wishlist


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


class WishlistView(DetailView):
    model = Product

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AddWishListForm(request.POST)
        obj = self.get_object()
        if form.is_valid():
            wishlist = form.save(commit=False)
            wishlist.product = obj
            wishlist.user = request.user
            wishlist.save()
        return HttpResponseRedirect(obj.get_absolute_url())
    

class RemoveFromWishlistView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        wish_id = kwargs.get('pk')
        try:
            wish = WishList.objects.get(pk=wish_id)
            wish.delete()
        except WishList.DoesNotExist:
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(reverse_lazy("account:profile"))

# Category


class CategoryFilter(FilterSet):
    class Meta:
        model = Product
        fields = {"title": ["contains"], "provider": ["exact"], "is_active": ["exact"]}


class CategoryListView(FilterView):
    filterset_class = CategoryFilter
    model = Product
    context_object_name = "products"
    paginate_by = 10
    template_name = "products/category.html"
    
    @method_decorator(cache_page(60 * 2))
    def dispatch(self, request, *args, **kwargs):
        print('loooool')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        slug = self.kwargs["category"]
        return Product.objects.filter(category__slug=slug).annotate(avg_rate=Avg("reviews__rate")).order_by("title")


class CategoryList(ListView):  # just to show the list of categories in one page for the user
    template_name = "products/category_list.html"
    context_object_name = "categories"
    queryset = Category.objects.all()
