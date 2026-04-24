import uuid

import pytest
from django.http import Http404

from posts.models import Like, Post
from posts.service.like_service import toggle_like
from tests.factories import TipPostFactory, UserFactory


@pytest.mark.django_db
class TestToggleLike:
    def test_좋아요_추가(self):
        user = UserFactory()
        post = TipPostFactory(like_count=0)

        is_liked, like_count = toggle_like(user=user, post_id=post.id)

        assert is_liked is True
        assert like_count == 1
        assert Like.objects.filter(user=user, post=post).exists()

    def test_좋아요_취소(self):
        user = UserFactory()
        post = TipPostFactory(like_count=1)
        Like.objects.create(user=user, post=post)

        is_liked, like_count = toggle_like(user=user, post_id=post.id)

        assert is_liked is False
        assert like_count == 0
        assert not Like.objects.filter(user=user, post=post).exists()

    def test_like_count_정확성(self):
        user1 = UserFactory()
        user2 = UserFactory()
        post = TipPostFactory(like_count=0)

        toggle_like(user=user1, post_id=post.id)
        toggle_like(user=user2, post_id=post.id)

        post.refresh_from_db()
        assert post.like_count == 2

    def test_좋아요_토글_on_off_반복(self):
        user = UserFactory()
        post = TipPostFactory(like_count=0)

        is_liked, count = toggle_like(user=user, post_id=post.id)
        assert is_liked is True
        assert count == 1

        is_liked, count = toggle_like(user=user, post_id=post.id)
        assert is_liked is False
        assert count == 0

    def test_존재하지_않는_게시글_좋아요_404(self):
        user = UserFactory()

        with pytest.raises(Http404):
            toggle_like(user=user, post_id=uuid.uuid4())
