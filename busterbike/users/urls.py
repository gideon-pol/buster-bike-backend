from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import DeleteView, ReferralCreateView, ReferralListView, ReservedBikeView, ReservedBikeEndView, RegisterView, MeView, LogoutView

urlpatterns = [
    path('reserved/end/', ReservedBikeEndView.as_view(), name='reserved'),
    path('reserved/', ReservedBikeView.as_view(), name='reserved'),
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('referral/', ReferralListView.as_view(), name='referral_list'),
    path('referral/create/', ReferralCreateView.as_view(), name='referral_create'),
    path('me/', MeView.as_view(), name='me'),
    path('delete/', DeleteView.as_view(), name='delete'),
]
