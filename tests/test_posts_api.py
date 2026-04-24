import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from posts.models import Like, Post
from tests.factories import (
    CommentFactory,
    MajorFactory,
    MajorPostFactory,
    TipPostFactory,
    UserFactory,
)


def auth_client(user):
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")
    return client


@pytest.fixture
def user():
    return UserFactory(password_hash=make_password("pass"))


@pytest.fixture
def client(user):
    return auth_client(user)


@pytest.fixture
def anon_client():
    return APIClient()


# ──────────────────────────────────────────
# TIP 게시글
# ──────────────────────────────────────────

@pytest.mark.django_db
class TestTipAPI:
    def test_TIP_목록_조회(self, anon_client):
        TipPostFactory.create_batch(3)

        resp = anon_client.get("/posts/tips/")

        assert resp.status_code == 200
        assert resp.data["count"] >= 3

    def test_TIP_카테고리_필터(self, anon_client):
        TipPostFactory(category="PLACE")
        TipPostFactory(category="DORM_LIFE")

        resp = anon_client.get("/posts/tips/?category=PLACE")

        assert resp.status_code == 200
        for item in resp.data["results"]:
            assert item["category"] == "PLACE"

    def test_TIP_생성_성공(self, client):
        resp = client.post(
            "/posts/tips/create/",
            {
                "title": "테스트 꿀팁",
                "body": "꿀팁 내용입니다",
                "category": "DORM_LIFE",
                "is_anonymous": False,
            },
            format="json",
        )

        assert resp.status_code == 201
        assert resp.data["title"] == "테스트 꿀팁"

    def test_TIP_생성_미인증_401(self, anon_client):
        resp = anon_client.post(
            "/posts/tips/create/",
            {"title": "제목", "body": "내용", "category": "ETC", "is_anonymous": False},
            format="json",
        )

        assert resp.status_code == 401

    def test_TIP_상세_조회(self, anon_client):
        post = TipPostFactory()

        resp = anon_client.get(f"/posts/tips/{post.id}/")

        assert resp.status_code == 200
        assert str(resp.data["id"]) == str(post.id)

    def test_TIP_삭제_본인(self, client, user):
        post = TipPostFactory(author=user)

        resp = client.delete(f"/posts/tips/{post.id}/delete/")

        assert resp.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()

    def test_TIP_삭제_타인_400(self, user):
        other = UserFactory()
        post = TipPostFactory(author=other)
        c = auth_client(user)

        resp = c.delete(f"/posts/tips/{post.id}/delete/")

        assert resp.status_code == 400


# ──────────────────────────────────────────
# MAJOR 게시글
# ──────────────────────────────────────────

@pytest.mark.django_db
class TestMajorCreateAPI:
    def test_전공_생성_성공(self, client):
        resp = client.post("/majors/create/", {"name": "백엔드"}, format="json")

        assert resp.status_code == 201
        assert resp.data["name"] == "백엔드"
        assert "id" in resp.data

    def test_전공_중복_생성_실패(self, client):
        MajorFactory(major="프론트엔드")

        resp = client.post("/majors/create/", {"name": "프론트엔드"}, format="json")

        assert resp.status_code == 400

    def test_전공_생성_미인증_401(self, anon_client):
        resp = anon_client.post("/majors/create/", {"name": "AI"}, format="json")

        assert resp.status_code == 401

    def test_전공_이름_필수(self, client):
        resp = client.post("/majors/create/", {}, format="json")

        assert resp.status_code == 400


@pytest.mark.django_db
class TestMajorPostAPI:
    def test_MAJOR_목록_조회(self, anon_client):
        MajorPostFactory.create_batch(2)

        resp = anon_client.get("/posts/major/")

        assert resp.status_code == 200
        assert resp.data["count"] >= 2

    def test_MAJOR_게시글_생성(self, client):
        major1 = MajorFactory()
        major2 = MajorFactory()

        resp = client.post(
            "/posts/major/create/",
            {
                "title": "전공 게시글",
                "body": "전공 내용",
                "major_ids": [str(major1.id), str(major2.id)],
                "is_anonymous": False,
            },
            format="json",
        )

        assert resp.status_code == 201
        assert resp.data["title"] == "전공 게시글"

    def test_MAJOR_게시글_삭제_본인(self, client, user):
        post = MajorPostFactory(author=user)

        resp = client.delete(f"/posts/major/{post.id}/delete/")

        assert resp.status_code == 204


# ──────────────────────────────────────────
# 댓글
# ──────────────────────────────────────────

@pytest.mark.django_db
class TestCommentAPI:
    def test_댓글_작성(self, client):
        post = TipPostFactory()

        resp = client.post(
            f"/posts/{post.id}/comments/",
            {"content": "좋은 글이에요", "is_anonymous": False},
            format="json",
        )

        assert resp.status_code == 201
        assert resp.data["content"] == "좋은 글이에요"

    def test_대댓글_작성(self, client):
        post = TipPostFactory()
        comment = CommentFactory(post=post)

        resp = client.post(
            f"/posts/{post.id}/comments/{comment.id}/replies/",
            {"content": "대댓글입니다", "is_anonymous": False},
            format="json",
        )

        assert resp.status_code == 201

    def test_댓글_삭제_본인(self, client, user):
        post = TipPostFactory()
        comment = CommentFactory(author=user, post=post)

        resp = client.delete(f"/posts/{post.id}/comments/{comment.id}/delete/")

        assert resp.status_code == 204

    def test_댓글_삭제_타인_400(self, user):
        other = UserFactory()
        post = TipPostFactory()
        comment = CommentFactory(author=other, post=post)
        c = auth_client(user)

        resp = c.delete(f"/posts/{post.id}/comments/{comment.id}/delete/")

        assert resp.status_code == 400


# ──────────────────────────────────────────
# 좋아요
# ──────────────────────────────────────────

@pytest.mark.django_db
class TestLikeAPI:
    def test_좋아요_토글_추가(self, client):
        post = TipPostFactory(like_count=0)

        resp = client.post(f"/posts/{post.id}/like/")

        assert resp.status_code == 200
        assert resp.data["is_liked"] is True
        assert resp.data["like_count"] == 1

    def test_좋아요_토글_취소(self, client, user):
        post = TipPostFactory(like_count=1)
        Like.objects.create(user=user, post=post)

        resp = client.post(f"/posts/{post.id}/like/")

        assert resp.status_code == 200
        assert resp.data["is_liked"] is False
        assert resp.data["like_count"] == 0

    def test_좋아요_미인증_401(self, anon_client):
        post = TipPostFactory()

        resp = anon_client.post(f"/posts/{post.id}/like/")

        assert resp.status_code == 401
