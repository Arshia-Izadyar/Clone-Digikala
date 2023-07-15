from django.urls import path, include

from .views import UserProfile, UserCreateAddress, UserUpdateAddress, UserDeleteAddress, CustomPasswordChangeView

app_name = 'account'

urlpatterns = [
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/addr/', UserCreateAddress.as_view(), name='address-create'),
    path('profile/addr/<int:pk>/update/', UserUpdateAddress.as_view(), name='address-update'),
    path('profile/addr/<int:pk>/delete/', UserDeleteAddress.as_view(), name='address-delete'),
    path('password/change/', CustomPasswordChangeView.as_view(), name="account_change_password"),
]
