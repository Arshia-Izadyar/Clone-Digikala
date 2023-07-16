from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .forms import UserAddressForm
from .models import UserAddress

from transaction.models import Wallet, Transaction

User = get_user_model()


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = "account/user_profile.html"
    model = User
    content_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not hasattr(self, "user_object"):
            self.user_object = User.objects.prefetch_related("reviews", "wishlists", "user_address", "wallet").get(
                pk=self.request.user.pk
            )

        Transaction.calc_score(self.user_object)
        Wallet.update_wallet(self.user_object)
        context["wallet"] = self.user_object.wallet
        context["user"] = self.user_object
        context["reviews"] = self.user_object.reviews.all()
        context["wishlists"] = self.user_object.wishlists.all()
        context["user_address"] = self.user_object.user_address.all()

        return context


class UserCreateAddress(LoginRequiredMixin, CreateView):
    form_class = UserAddressForm
    model = UserAddress
    template_name = "account/create_address.html"
    # success_url = reverse_lazy("account:profile")

    def form_valid(self, form):
        addr = form.save(commit=False)
        addr.user = self.request.user
        addr.save()
        return HttpResponseRedirect(reverse_lazy("account:profile"))

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class UserUpdateAddress(LoginRequiredMixin, UpdateView):
    form_class = UserAddressForm
    model = UserAddress
    template_name = "account/update_address.html"
    success_url = reverse_lazy("account:profile")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class UserDeleteAddress(LoginRequiredMixin, DeleteView):
    model = UserAddress
    template_name = "account/delete_address.html"
    success_url = reverse_lazy("account:profile")
    context_object_name = "address"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


from allauth.account.views import PasswordChangeView


class CustomPasswordChangeView(PasswordChangeView):
    success_url = "/"
