import requests
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

from config.exceptions import InvalidCredentialsException
from users.models import User


class AuthService:
    DSM_LOGIN_URL = "https://dsm-login.dsmhs.kr/dsm-login/user/user-data"

    @staticmethod
    def login(*, account_id, password):
        # 1. 로컬 DB 확인
        try:
            user = User.objects.get(account_id=account_id)

            # 기존 유저: 비밀번호 해시 검증
            if not check_password(password, user.password_hash):
                raise InvalidCredentialsException()

        except User.DoesNotExist:
            # 2. 없으면 외부 DSM API 호출
            try:
                resp = requests.post(
                    AuthService.DSM_LOGIN_URL,
                    json={"account_id": account_id, "password": password},
                    timeout=10,
                )
            except requests.RequestException as exc:
                raise InvalidCredentialsException() from exc

            if resp.status_code != 200:
                raise InvalidCredentialsException()

            data = resp.json()

            # 3. 로컬 DB에 유저 생성 (비밀번호 해시하여 저장)
            student_id = f"{data['grade']}-{data['class_num']}-{data['num']}"
            user = User.objects.create(
                account_id=data["account_id"],
                student_id=student_id,
                grade=data["grade"],
                class_num=data["class_num"],
                num=data["num"],
                name=data["name"],
                password_hash=make_password(password),
            )

        # 4. JWT 발급
        refresh = RefreshToken.for_user(user)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": str(user.id),
                "account_id": user.account_id,
                "name": user.name,
                "grade": user.grade,
                "class_num": user.class_num,
                "num": user.num,
            },
        }
