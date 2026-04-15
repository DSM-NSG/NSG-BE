from rest_framework_simplejwt.tokens import RefreshToken

from config.exceptions import InvalidCredentialsException
from users.models import User


class AuthService:
    @staticmethod
    def login(*, grade, class_num, num, password):
        try:
            user = User.objects.get(
                grade=grade,
                class_num=class_num,
                num=num,
            )
        except User.DoesNotExist as exc:
            raise InvalidCredentialsException() from exc

        if not user.check_password(password):
            raise InvalidCredentialsException()

        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user": {
                "id": str(user.id),
                "grade": user.grade,
                "class_num": user.class_num,
                "num": user.num,
                "name": user.name,
                "cohort": user.cohort,
            },
        }
