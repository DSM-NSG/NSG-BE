from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "요청 처리 중 오류가 발생했습니다."
    default_code = "application_error"


class InvalidCredentialsException(CustomAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "학번 또는 비밀번호가 올바르지 않습니다."
    default_code = "invalid_credentials"
