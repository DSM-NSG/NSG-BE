from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.exceptions import CustomAPIException
from places.apis.serializers import PlaceCreateSerializer, PlaceSerializer
from places.models import Place
from places.service.place_service import create_place, delete_place
from posts.models import Post
from posts.apis.serializers import TipListSerializer


class PlaceView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    @extend_schema(
        summary="장소 목록",
        tags=["Places"],
        parameters=[
            OpenApiParameter(name='category', description='카테고리 필터', required=False, type=str),
        ],
        responses={200: PlaceSerializer(many=True)},
    )
    def get(self, request):
        category = request.query_params.get('category')
        qs = Place.objects.select_related('author').order_by('-created_at')
        if category:
            qs = qs.filter(category=category)
        return Response(PlaceSerializer(qs, many=True).data)

    @extend_schema(
        summary="장소 등록",
        tags=["Places"],
        request=PlaceCreateSerializer,
        responses={201: PlaceSerializer},
    )
    def post(self, request):
        serializer = PlaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        place = create_place(user=request.user, **serializer.validated_data)
        return Response(PlaceSerializer(place).data, status=status.HTTP_201_CREATED)


class PlaceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="장소 삭제",
        tags=["Places"],
        responses={204: None},
    )
    def delete(self, request, pk):
        try:
            delete_place(user=request.user, place_id=pk)
        except PermissionError:
            raise CustomAPIException("본인의 장소만 삭제할 수 있습니다.")
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlacePostsView(APIView):
    @extend_schema(
        summary="장소별 게시글 목록",
        tags=["Places"],
        responses={200: TipListSerializer(many=True)},
    )
    def get(self, request, pk):
        qs = (
            Post.objects.filter(place_id=pk, post_type='TIP')
            .select_related('author')
            .prefetch_related('anonymous_users', 'images', 'likes')
            .order_by('-created_at')
        )
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(qs, request)
        serializer = TipListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
