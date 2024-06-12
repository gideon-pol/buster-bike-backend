from django.urls import path

from .views import ListBikesView, ReserveBikeView, ImageBikeView

urlpatterns = [
    path('list/', ListBikesView.as_view(), name='list_bikes'),
    path('image/<uuid:bike_id>/', ImageBikeView.as_view(), name='bike_image'),
    path('reserve/<uuid:bike_id>/', ReserveBikeView.as_view(), name='reserve_bike'),
]
