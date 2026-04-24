from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth.hashers import make_password

from config.exceptions import InvalidCredentialsException
from tests.factories import UserFactory
from users.service.auth_service import AuthService


@pytest.mark.django_db
class TestAuthServiceLogin:
    def test_로컬_유저_로그인_성공(self):
        user = UserFactory(password_hash=make_password("correct_pass"))

        result = AuthService.login(account_id=user.account_id, password="correct_pass")

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["user"]["account_id"] == user.account_id

    def test_비밀번호_불일치_실패(self):
        user = UserFactory(password_hash=make_password("correct_pass"))

        with pytest.raises(InvalidCredentialsException):
            AuthService.login(account_id=user.account_id, password="wrong_pass")

    def test_DSM_API_호출_후_유저_생성(self):
        dsm_response = MagicMock()
        dsm_response.status_code = 200
        dsm_response.json.return_value = {
            "account_id": "newuser001",
            "grade": 2,
            "class_num": 3,
            "num": 5,
            "name": "김테스트",
        }

        with patch("users.service.auth_service.requests.post", return_value=dsm_response):
            result = AuthService.login(account_id="newuser001", password="any_pass")

        assert result["user"]["account_id"] == "newuser001"
        assert result["user"]["name"] == "김테스트"
        assert "access_token" in result

    def test_DSM_API_실패시_예외(self):
        dsm_response = MagicMock()
        dsm_response.status_code = 401

        with patch("users.service.auth_service.requests.post", return_value=dsm_response):
            with pytest.raises(InvalidCredentialsException):
                AuthService.login(account_id="nouser", password="pass")

    def test_DSM_API_네트워크_오류시_예외(self):
        import requests as req

        with patch(
            "users.service.auth_service.requests.post",
            side_effect=req.RequestException("timeout"),
        ):
            with pytest.raises(InvalidCredentialsException):
                AuthService.login(account_id="nouser", password="pass")

    def test_cohort_계산(self):
        """cohort가 없는 유저 로그인 시 자동 계산"""
        user = UserFactory(
            password_hash=make_password("pass"),
            cohort=None,
            grade=2,
        )

        result = AuthService.login(account_id=user.account_id, password="pass")

        user.refresh_from_db()
        assert user.cohort is not None
        assert "access_token" in result
