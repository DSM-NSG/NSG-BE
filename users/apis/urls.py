from django.urls import path

from users.apis.views import LoginView, UserTestView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("test/", UserTestView.as_view(), name="user-test"),
]
