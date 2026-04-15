from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import status, serializers as drf_serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.exceptions import CustomAPIException
from posts.apis.serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    MajorPostCreateSerializer,
    MajorPostDetailSerializer,
    MajorPostListSerializer,
    MajorSerializer,
    ReplySerializer,
    TipCreateSerializer,
    TipDetailSerializer,
    TipListSerializer,
)
from posts.models import Major, Post
from posts.service.comment_service import create_comment, create_reply, delete_comment
from posts.service.like_service import toggle_like
from posts.service.post_service import create_major_post, create_tip, delete_post


# ──────────────────────────────────────────
# Majors
# ──────────────────────────────────────────

class MajorListView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="전공 카테고리 목록",
        tags=["Majors"],
        responses={200: MajorSerializer(many=True)},
    )
    def get(self, request):
        majors = Major.objects.order_by('major')
        return Response(MajorSerializer(majors, many=True).data)


# ──────────────────────────────────────────
# TIP 게시글
# ──────────────────────────────────────────

class TipListView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="꿀팁 게시글 목록",
        tags=["Tips"],
        parameters=[
            OpenApiParameter(name='category', description='카테고리 필터', required=False, type=str),
            OpenApiParameter(name='search', description='제목 검색', required=False, type=str),
            OpenApiParameter(name='page', description='페이지 번호', required=False, type=int),
        ],
        responses={200: TipListSerializer(many=True)},
    )
    def get(self, request):
        category = request.query_params.get('category')
        search = request.query_params.get('search')

        qs = (
            Post.objects.filter(post_type='TIP')
            .select_related('author')
            .prefetch_related('anonymous_users', 'images', 'comments')
            .order_by('-created_at')
        )
        if category:
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(title__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(TipListSerializer(page, many=True).data)


class TipCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="꿀팁 게시글 작성",
        tags=["Tips"],
        request=TipCreateSerializer,
        responses={201: TipDetailSerializer},
    )
    def post(self, request):
        serializer = TipCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = create_tip(user=request.user, **serializer.validated_data)
        post = (
            Post.objects.select_related('author', 'place')
            .prefetch_related('anonymous_users', 'images', 'comments')
            .get(pk=post.pk)
        )
        return Response(
            TipDetailSerializer(post, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class TipDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="꿀팁 게시글 상세",
        tags=["Tips"],
        responses={200: TipDetailSerializer},
    )
    def get(self, request, pk):
        post = get_object_or_404(
            Post.objects.select_related('author', 'place')
            .prefetch_related('anonymous_users', 'images', 'likes', 'comments__author', 'comments__replies__author'),
            pk=pk,
            post_type='TIP',
        )
        return Response(TipDetailSerializer(post, context={'request': request}).data)


class TipDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="꿀팁 게시글 삭제",
        tags=["Tips"],
        responses={204: None},
    )
    def delete(self, request, pk):
        try:
            delete_post(user=request.user, post_id=pk, post_type='TIP')
        except PermissionError:
            raise CustomAPIException("본인의 게시글만 삭제할 수 있습니다.")
        return Response(status=status.HTTP_204_NO_CONTENT)


# ──────────────────────────────────────────
# MAJOR 게시글
# ──────────────────────────────────────────

class MajorPostListView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="전공 게시글 목록",
        tags=["Major Posts"],
        parameters=[
            OpenApiParameter(name='major_id', description='전공 ID 필터', required=False, type=str),
            OpenApiParameter(name='search', description='제목 검색', required=False, type=str),
            OpenApiParameter(name='page', description='페이지 번호', required=False, type=int),
        ],
        responses={200: MajorPostListSerializer(many=True)},
    )
    def get(self, request):
        major_id = request.query_params.get('major_id')
        search = request.query_params.get('search')

        qs = (
            Post.objects.filter(post_type='MAJOR')
            .select_related('author')
            .prefetch_related('anonymous_users', 'major_tags__major', 'comments')
            .order_by('-created_at')
        )
        if major_id:
            qs = qs.filter(major_tags__major_id=major_id)
        if search:
            qs = qs.filter(title__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(MajorPostListSerializer(page, many=True).data)


class MajorPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="전공 게시글 작성",
        tags=["Major Posts"],
        request=MajorPostCreateSerializer,
        responses={201: MajorPostDetailSerializer},
    )
    def post(self, request):
        serializer = MajorPostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = create_major_post(user=request.user, **serializer.validated_data)
        post = (
            Post.objects.select_related('author')
            .prefetch_related('anonymous_users', 'major_tags__major', 'images', 'comments')
            .get(pk=post.pk)
        )
        return Response(
            MajorPostDetailSerializer(post, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class MajorPostDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="전공 게시글 상세",
        tags=["Major Posts"],
        responses={200: MajorPostDetailSerializer},
    )
    def get(self, request, pk):
        post = get_object_or_404(
            Post.objects.select_related('author')
            .prefetch_related(
                'anonymous_users', 'major_tags__major', 'images',
                'likes', 'comments__author', 'comments__replies__author',
            ),
            pk=pk,
            post_type='MAJOR',
        )
        return Response(MajorPostDetailSerializer(post, context={'request': request}).data)


class MajorPostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="전공 게시글 삭제",
        tags=["Major Posts"],
        responses={204: None},
    )
    def delete(self, request, pk):
        try:
            delete_post(user=request.user, post_id=pk, post_type='MAJOR')
        except PermissionError:
            raise CustomAPIException("본인의 게시글만 삭제할 수 있습니다.")
        return Response(status=status.HTTP_204_NO_CONTENT)


# ──────────────────────────────────────────
# 댓글 / 대댓글
# ──────────────────────────────────────────

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="댓글 작성",
        tags=["Comments"],
        request=CommentCreateSerializer,
        responses={201: CommentSerializer},
    )
    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = create_comment(user=request.user, post_id=post_id, **serializer.validated_data)

        post = comment.post
        post.anonymous_users.all()
        return Response(
            CommentSerializer(comment, context={'post': post}).data,
            status=status.HTTP_201_CREATED,
        )


class ReplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="대댓글 작성",
        tags=["Comments"],
        request=CommentCreateSerializer,
        responses={201: ReplySerializer},
    )
    def post(self, request, post_id, comment_id):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reply = create_reply(
            user=request.user, post_id=post_id, comment_id=comment_id, **serializer.validated_data
        )

        post = reply.post
        post.anonymous_users.all()
        return Response(
            ReplySerializer(reply, context={'post': post}).data,
            status=status.HTTP_201_CREATED,
        )


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="댓글 삭제",
        tags=["Comments"],
        responses={204: None},
    )
    def delete(self, request, post_id, comment_id):
        try:
            delete_comment(user=request.user, post_id=post_id, comment_id=comment_id)
        except PermissionError:
            raise CustomAPIException("본인의 댓글만 삭제할 수 있습니다.")
        return Response(status=status.HTTP_204_NO_CONTENT)


# ──────────────────────────────────────────
# 좋아요
# ──────────────────────────────────────────

class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="좋아요 토글",
        tags=["Likes"],
        request=None,
        responses={
            200: inline_serializer(
                name='LikeToggleResponse',
                fields={
                    'is_liked': drf_serializers.BooleanField(),
                    'like_count': drf_serializers.IntegerField(),
                },
            )
        },
    )
    def post(self, request, post_id):
        is_liked, like_count = toggle_like(user=request.user, post_id=post_id)
        return Response({"is_liked": is_liked, "like_count": like_count})
