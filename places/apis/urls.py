from django.urls import path

from places.apis.views import PlaceDetailView, PlaceView

urlpatterns = [
    path('', PlaceView.as_view(), name='place-list-create'),
    path('<uuid:pk>/', PlaceDetailView.as_view(), name='place-delete'),
]
