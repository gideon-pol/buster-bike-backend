from django.urls import path

from .views import ReservedBikeView, ReservedBikeEndView

urlpatterns = [
    path('reserved/end', ReservedBikeEndView.as_view(), name='reserved'),
    path('reserved', ReservedBikeView.as_view(), name='reserved')


]
