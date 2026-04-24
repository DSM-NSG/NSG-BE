from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.apis.serializer import LoginSerializer, LoginResponseSerializer, MyPageSerializer, UserTestSerializer
from users.service.auth_service import AuthService
from users.service.user_service import withdraw_user


class MyPageView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MyPageSerializer},
        summary="마이페이지 조회",
        tags=["Users"],
    )
    def get(self, request):
        serializer = MyPageSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTestView(APIView):
    def post(self, request):
        serializer = UserTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data["name"]
        return Response(
            {"message": f"{name}"},
            status=status.HTTP_200_OK,
        )


class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="회원탈퇴",
        tags=["Users"],
        responses={204: None},
    )
    def delete(self, request):
        withdraw_user(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
