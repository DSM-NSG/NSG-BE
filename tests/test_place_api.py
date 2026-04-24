import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests.factories import PlaceFactory, TipPostFactory, UserFactory


def auth_client(user):
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")
    return client


@pytest.fixture
def anon_client():
    return APIClient()


@pytest.mark.django_db
class TestPlacePostsAPI:
    def test_장소별_게시글_목록_조회(self, anon_client):
        place = PlaceFactory()
        TipPostFactory.create_batch(3, place=place)
        TipPostFactory(place=None)  # 다른 장소 게시글 (조회 안 됨)

        resp = anon_client.get(f"/{place.id}/posts/")

        assert resp.status_code == 200
        assert resp.data["count"] == 3

    def test_장소에_게시글_없으면_빈_리스트(self, anon_client):
        place = PlaceFactory()

        resp = anon_client.get(f"/{place.id}/posts/")

        assert resp.status_code == 200
        assert resp.data["count"] == 0
        assert resp.data["results"] == []

    def test_다른_장소_게시글_포함_안됨(self, anon_client):
        place1 = PlaceFactory()
        place2 = PlaceFactory()
        TipPostFactory.create_batch(2, place=place1)
        TipPostFactory(place=place2)

        resp = anon_client.get(f"/{place1.id}/posts/")

        assert resp.status_code == 200
        assert resp.data["count"] == 2

    def test_MAJOR_게시글_포함_안됨(self, anon_client):
        from tests.factories import MajorPostFactory
        place = PlaceFactory()
        TipPostFactory(place=place)
        MajorPostFactory(place=place)

        resp = anon_client.get(f"/{place.id}/posts/")

        assert resp.status_code == 200
        assert resp.data["count"] == 1
