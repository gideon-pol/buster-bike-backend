from django.urls import path

from .views import ListBikesView, ReserveBikeView

urlpatterns = [
    path('list/', ListBikesView.as_view(), name='list_bikes'),
    path('reserve/<uuid:bike_id>/', ReserveBikeView.as_view(), name='reserve_bike'),
]
