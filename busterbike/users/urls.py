from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import ReservedBikeView, ReservedBikeEndView, RegisterView

urlpatterns = [
    path('reserved/end/', ReservedBikeEndView.as_view(), name='reserved'),
    path('reserved/', ReservedBikeView.as_view(), name='reserved'),
    path('login/', obtain_auth_token),
    path('register/', RegisterView.as_view(), name='register'),
]
