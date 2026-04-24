import pytest

from posts.models import MajorTag, Post, PostImage
from posts.service.post_service import (
    create_major_post,
    create_tip,
    delete_post,
    get_popular_major_tags,
)
from tests.factories import MajorFactory, MajorPostFactory, TipPostFactory, UserFactory


@pytest.mark.django_db
class TestCreateTip:
    def test_기본_TIP_생성(self):
        user = UserFactory()

        post = create_tip(
            user=user,
            title="꿀팁 제목",
            body="꿀팁 내용",
            category="DORM_LIFE",
            is_anonymous=False,
        )

        assert post.post_type == "TIP"
        assert post.author == user
        assert post.category == "DORM_LIFE"

    def test_익명_TIP_생성시_익명순번_생성(self):
        user = UserFactory()

        post = create_tip(
            user=user,
            title="익명 꿀팁",
            body="내용",
            category="ETC",
            is_anonymous=True,
        )

        assert post.is_anonymous is True
        assert post.anonymous_users.filter(user=user).exists()

    def test_이미지_URL_포함_TIP_생성(self):
        user = UserFactory()
        urls = ["https://s3.example.com/img1.jpg", "https://s3.example.com/img2.jpg"]

        post = create_tip(
            user=user,
            title="이미지 있는 꿀팁",
            body="내용",
            category="PLACE",
            is_anonymous=False,
            image_urls=urls,
        )

        images = PostImage.objects.filter(post=post).order_by("order_index")
        assert images.count() == 2
        assert images[0].image_url == urls[0]
        assert images[1].image_url == urls[1]


@pytest.mark.django_db
class TestCreateMajorPost:
    def test_기본_MAJOR_게시글_생성(self):
        user = UserFactory()
        major1 = MajorFactory()
        major2 = MajorFactory()

        post = create_major_post(
            user=user,
            title="전공 게시글",
            body="내용",
            major_ids=[major1.id, major2.id],
            is_anonymous=False,
        )

        assert post.post_type == "MAJOR"
        assert MajorTag.objects.filter(post=post).count() == 2

    def test_익명_MAJOR_게시글_생성(self):
        user = UserFactory()
        major = MajorFactory()

        post = create_major_post(
            user=user,
            title="익명 전공 게시글",
            body="내용",
            major_ids=[major.id],
            is_anonymous=True,
        )

        assert post.is_anonymous is True
        assert post.anonymous_users.filter(user=user).exists()


@pytest.mark.django_db
class TestDeletePost:
    def test_본인_게시글_삭제_성공(self):
        user = UserFactory()
        post = TipPostFactory(author=user)

        delete_post(user=user, post_id=post.id, post_type="TIP")

        assert not Post.objects.filter(id=post.id).exists()

    def test_타인_게시글_삭제_실패(self):
        owner = UserFactory()
        other = UserFactory()
        post = TipPostFactory(author=owner)

        with pytest.raises(PermissionError):
            delete_post(user=other, post_id=post.id, post_type="TIP")

    def test_존재하지_않는_게시글_삭제_404(self):
        import uuid
        from django.http import Http404

        user = UserFactory()

        with pytest.raises(Http404):
            delete_post(user=user, post_id=uuid.uuid4(), post_type="TIP")


@pytest.mark.django_db
class TestGetPopularMajorTags:
    def test_인기태그_반환(self):
        user = UserFactory()
        major = MajorFactory()
        post = MajorPostFactory(author=user, like_count=5)
        MajorTag.objects.create(post=post, major=major)

        result = get_popular_major_tags(top_n=10)

        assert len(result) >= 1
        assert result[0]["major"] is not None
        assert result[0]["score"] > 0

    def test_top_n_제한(self):
        user = UserFactory()
        for _ in range(5):
            major = MajorFactory()
            post = MajorPostFactory(author=user)
            MajorTag.objects.create(post=post, major=major)

        result = get_popular_major_tags(top_n=3)

        assert len(result) <= 3

    def test_게시글_없어도_전공은_반환(self):
        MajorFactory.create_batch(3)

        result = get_popular_major_tags(top_n=10)

        assert len(result) == 3
        assert all(r['score'] == 0.0 for r in result)
        assert all(r['post_count'] == 0 for r in result)

    def test_게시글도_전공도_없으면_빈_리스트(self):
        result = get_popular_major_tags(top_n=10)
        assert result == []
