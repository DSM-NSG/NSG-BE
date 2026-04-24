from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from tests.factories import UserFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
class TestLoginAPI:
    def test_로컬_유저_로그인_성공(self, client):
        user = UserFactory(
            account_id="testuser01",
            password_hash=make_password("pass1234!"),
        )

        resp = client.post(
            "/users/login/",
            {"account_id": "testuser01", "password": "pass1234!"},
            format="json",
        )

        assert resp.status_code == 200
        assert "access_token" in resp.data
        assert "refresh_token" in resp.data
        assert resp.data["user"]["account_id"] == "testuser01"

    def test_비밀번호_틀리면_401(self, client):
        UserFactory(
            account_id="testuser02",
            password_hash=make_password("correct!"),
        )

        with patch(
            "users.service.auth_service.requests.post",
            return_value=MagicMock(status_code=401),
        ):
            resp = client.post(
                "/users/login/",
                {"account_id": "testuser02", "password": "wrong!"},
                format="json",
            )

        assert resp.status_code == 401

    def test_존재하지_않는_유저_DSM_API_호출(self, client):
        dsm_resp = MagicMock()
        dsm_resp.status_code = 200
        dsm_resp.json.return_value = {
            "account_id": "newstudent",
            "grade": 1,
            "class_num": 2,
            "num": 3,
            "name": "신입생",
        }

        with patch("users.service.auth_service.requests.post", return_value=dsm_resp):
            resp = client.post(
                "/users/login/",
                {"account_id": "newstudent", "password": "anypass"},
                format="json",
            )

        assert resp.status_code == 200
        assert resp.data["user"]["name"] == "신입생"

    def test_필수_필드_누락_400(self, client):
        resp = client.post("/users/login/", {"account_id": "only"}, format="json")

        assert resp.status_code == 400

    def test_인증_후_마이페이지_조회(self, client):
        user = UserFactory(password_hash=make_password("mypass!"))

        login_resp = client.post(
            "/users/login/",
            {"account_id": user.account_id, "password": "mypass!"},
            format="json",
        )
        token = login_resp.data["access_token"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        resp = client.get("/users/me/")

        assert resp.status_code == 200
        assert str(resp.data["user_id"]) == str(user.id)
        assert resp.data["grade"] == user.grade
