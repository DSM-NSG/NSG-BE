from django.urls import path

from users.apis.views import LoginView, MyPageView, UserTestView, WithdrawView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MyPageView.as_view(), name="my-page"),
    path("me/withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("test/", UserTestView.as_view(), name="user-test"),
]
