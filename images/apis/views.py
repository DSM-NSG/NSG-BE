from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from images.apis.serializers import ImageUploadSerializer, ImageUploadResponseSerializer
from images.service.image_service import ImageService


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @extend_schema(
        request=ImageUploadSerializer,
        responses={200: ImageUploadResponseSerializer},
        summary="이미지 업로드",
        tags=["Images"],
    )
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = ImageService.upload(serializer.validated_data["image"])
        return Response({"url": url}, status=status.HTTP_200_OK)
