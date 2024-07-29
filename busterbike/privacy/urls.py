from django.urls import path

from .views import DeleteAccountView, PrivacyView

urlpatterns = [
    path('delete/', DeleteAccountView.as_view()),
    path('', PrivacyView.as_view()),
]
