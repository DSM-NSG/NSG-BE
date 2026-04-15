from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.exceptions import CustomAPIException
from posts.apis.serializers import (
    CommentCreateSerializer,
    MajorPostCreateSerializer,
    MajorPostDetailSerializer,
    MajorPostListSerializer,
    MajorSerializer,
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

    def get(self, request):
        majors = Major.objects.order_by('major')
        return Response(MajorSerializer(majors, many=True).data)


# ──────────────────────────────────────────
# TIP 게시글
# ──────────────────────────────────────────

class TipListView(APIView):
    authentication_classes = []
    permission_classes = []

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

        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(TipListSerializer(page, many=True).data)


class TipCreateView(APIView):
    permission_classes = [IsAuthenticated]

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

        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(MajorPostListSerializer(page, many=True).data)


class MajorPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

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

    def post(self, request, post_id):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = create_comment(user=request.user, post_id=post_id, **serializer.validated_data)

        from posts.apis.serializers import CommentSerializer
        post = comment.post
        post.anonymous_users.all()  # trigger prefetch
        return Response(
            CommentSerializer(comment, context={'post': post}).data,
            status=status.HTTP_201_CREATED,
        )


class ReplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, comment_id):
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reply = create_reply(
            user=request.user, post_id=post_id, comment_id=comment_id, **serializer.validated_data
        )

        from posts.apis.serializers import ReplySerializer
        post = reply.post
        post.anonymous_users.all()
        return Response(
            ReplySerializer(reply, context={'post': post}).data,
            status=status.HTTP_201_CREATED,
        )


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

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

    def post(self, request, post_id):
        is_liked, like_count = toggle_like(user=request.user, post_id=post_id)
        return Response({"is_liked": is_liked, "like_count": like_count})
