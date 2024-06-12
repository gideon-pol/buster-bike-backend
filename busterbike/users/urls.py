from django.urls import path

from .views import ReservedBikeView

urlpatterns = [
    path('reserved', ReservedBikeView.as_view(), name='reserved')
]
