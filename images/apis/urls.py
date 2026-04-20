from django.urls import path

from images.apis.views import ImageUploadView

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="image-upload"),
]
