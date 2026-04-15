from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.apis.serializer import LoginSerializer, LoginResponseSerializer, UserTestSerializer
from users.service.auth_service import AuthService


class UserTestView(APIView):
    def post(self, request):
        serializer = UserTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data["name"]
        return Response(
            {"message": f"{name}"},
            status=status.HTTP_200_OK,
        )


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser]

    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginResponseSerializer},
        summary="로그인",
        tags=["Auth"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login_result = AuthService.login(**serializer.validated_data)

        return Response(login_result, status=status.HTTP_200_OK)
