import uuid

import pytest
from django.http import Http404

from posts.models import Comment
from posts.service.comment_service import create_comment, create_reply, delete_comment
from tests.factories import CommentFactory, TipPostFactory, UserFactory


@pytest.mark.django_db
class TestCreateComment:
    def test_댓글_생성_성공(self):
        user = UserFactory()
        post = TipPostFactory()

        comment = create_comment(
            user=user, post_id=post.id, content="좋은 꿀팁이네요!", is_anonymous=False
        )

        assert comment.post == post
        assert comment.author == user
        assert comment.content == "좋은 꿀팁이네요!"
        assert comment.parent is None

    def test_익명_댓글_생성(self):
        user = UserFactory()
        post = TipPostFactory()

        comment = create_comment(
            user=user, post_id=post.id, content="익명 댓글", is_anonymous=True
        )

        assert comment.is_anonymous is True
        assert post.anonymous_users.filter(user=user).exists()

    def test_존재하지_않는_게시글_댓글_404(self):
        user = UserFactory()

        with pytest.raises(Http404):
            create_comment(
                user=user, post_id=uuid.uuid4(), content="댓글", is_anonymous=False
            )


@pytest.mark.django_db
class TestCreateReply:
    def test_대댓글_생성_성공(self):
        user = UserFactory()
        post = TipPostFactory()
        parent_comment = CommentFactory(post=post)

        reply = create_reply(
            user=user,
            post_id=post.id,
            comment_id=parent_comment.id,
            content="대댓글입니다",
            is_anonymous=False,
        )

        assert reply.parent == parent_comment
        assert reply.post == post
        assert reply.content == "대댓글입니다"

    def test_대댓글에_대한_대댓글_불가(self):
        """대댓글(parent 있음)에는 대댓글 달기 불가 — get_object_or_404(parent=None) 조건"""
        user = UserFactory()
        post = TipPostFactory()
        parent = CommentFactory(post=post)
        reply = CommentFactory(post=post, parent=parent)

        with pytest.raises(Http404):
            create_reply(
                user=user,
                post_id=post.id,
                comment_id=reply.id,
                content="대대댓글",
                is_anonymous=False,
            )


@pytest.mark.django_db
class TestDeleteComment:
    def test_본인_댓글_삭제_성공(self):
        user = UserFactory()
        post = TipPostFactory()
        comment = CommentFactory(author=user, post=post)

        delete_comment(user=user, post_id=post.id, comment_id=comment.id)

        assert not Comment.objects.filter(id=comment.id).exists()

    def test_타인_댓글_삭제_실패(self):
        owner = UserFactory()
        other = UserFactory()
        post = TipPostFactory()
        comment = CommentFactory(author=owner, post=post)

        with pytest.raises(PermissionError):
            delete_comment(user=other, post_id=post.id, comment_id=comment.id)

    def test_존재하지_않는_댓글_삭제_404(self):
        user = UserFactory()
        post = TipPostFactory()

        with pytest.raises(Http404):
            delete_comment(user=user, post_id=post.id, comment_id=uuid.uuid4())
