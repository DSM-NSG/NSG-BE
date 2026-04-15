from django.urls import path

from posts.apis.views import (
    CommentCreateView,
    CommentDeleteView,
    LikeToggleView,
    MajorListView,
    MajorPostCreateView,
    MajorPostDeleteView,
    MajorPostDetailView,
    MajorPostListView,
    ReplyCreateView,
    TipCreateView,
    TipDeleteView,
    TipDetailView,
    TipListView,
)

urlpatterns = [
    # 전공 카테고리
    path('majors/', MajorListView.as_view(), name='major-list'),

    # 꿀팁 게시글
    path('posts/tips/', TipListView.as_view(), name='tip-list'),
    path('posts/tips/create/', TipCreateView.as_view(), name='tip-create'),
    path('posts/tips/<uuid:pk>/', TipDetailView.as_view(), name='tip-detail'),
    path('posts/tips/<uuid:pk>/delete/', TipDeleteView.as_view(), name='tip-delete'),

    # 전공 게시글
    path('posts/major/', MajorPostListView.as_view(), name='major-post-list'),
    path('posts/major/create/', MajorPostCreateView.as_view(), name='major-post-create'),
    path('posts/major/<uuid:pk>/', MajorPostDetailView.as_view(), name='major-post-detail'),
    path('posts/major/<uuid:pk>/delete/', MajorPostDeleteView.as_view(), name='major-post-delete'),

    # 댓글 / 대댓글
    path('posts/<uuid:post_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/<uuid:post_id>/comments/<uuid:comment_id>/replies/', ReplyCreateView.as_view(), name='reply-create'),
    path('posts/<uuid:post_id>/comments/<uuid:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # 좋아요
    path('posts/<uuid:post_id>/like/', LikeToggleView.as_view(), name='like-toggle'),
]
