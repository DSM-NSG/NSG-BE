import factory
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory

from places.models import Place
from posts.models import Comment, Like, Major, MajorTag, Post
from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    account_id = factory.Sequence(lambda n: f"user{n:04d}")
    student_id = factory.Sequence(lambda n: f"1-1-{n + 1}")
    grade = 1
    class_num = 1
    num = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("name", locale="ko_KR")
    cohort = 10
    is_active = True
    password_hash = factory.LazyFunction(lambda: make_password("testpass123!"))


class PlaceFactory(DjangoModelFactory):
    class Meta:
        model = Place

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("company", locale="ko_KR")
    description = factory.Faker("text", max_nb_chars=100, locale="ko_KR")
    category = "RESTAURANT"
    latitude = 36.3504
    longitude = 127.3845
    is_anonymous = False


class MajorFactory(DjangoModelFactory):
    class Meta:
        model = Major

    major = factory.Sequence(lambda n: f"전공{n}")


class TipPostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=5, locale="ko_KR")
    body = factory.Faker("text", max_nb_chars=200, locale="ko_KR")
    post_type = "TIP"
    category = "DORM_LIFE"
    is_anonymous = False
    like_count = 0


class MajorPostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=5, locale="ko_KR")
    body = factory.Faker("text", max_nb_chars=200, locale="ko_KR")
    post_type = "MAJOR"
    category = ""
    is_anonymous = False
    like_count = 0


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(TipPostFactory)
    content = factory.Faker("sentence", locale="ko_KR")
    is_anonymous = False


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(TipPostFactory)


class MajorTagFactory(DjangoModelFactory):
    class Meta:
        model = MajorTag

    post = factory.SubFactory(MajorPostFactory)
    major = factory.SubFactory(MajorFactory)
