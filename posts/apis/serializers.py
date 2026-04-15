from rest_framework import serializers

from posts.models import Post, PostImage, PostAnonymousUser, Comment, Major, MajorTag


# ──────────────────────────────────────────
# 공통 헬퍼
# ──────────────────────────────────────────

def _author_data(obj, post):
    """
    Post 또는 Comment 객체의 author 정보를 반환.
    익명이면 anonymous_number 반환, 실명이면 학번+이름 반환.
    post.anonymous_users가 prefetch된 상태를 가정.
    """
    if obj.author is None:
        return None
    if not obj.is_anonymous:
        return {
            "grade": obj.author.grade,
            "class_num": obj.author.class_num,
            "num": obj.author.num,
            "name": obj.author.name,
        }
    for au in post.anonymous_users.all():
        if au.user_id == obj.author.id:
            return {"anonymous_number": au.anonymous_number}
    return {"anonymous_number": 0}


# ──────────────────────────────────────────
# Major
# ──────────────────────────────────────────

class MajorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='major')

    class Meta:
        model = Major
        fields = ['id', 'name']


# ──────────────────────────────────────────
# PostImage
# ──────────────────────────────────────────

class PostImageSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='image_url')

    class Meta:
        model = PostImage
        fields = ['url', 'order_index']


# ──────────────────────────────────────────
# Comment / Reply
# ──────────────────────────────────────────

class ReplySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'is_anonymous', 'created_at']

    def get_author(self, obj):
        post = self.context.get('post')
        return _author_data(obj, post)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'is_anonymous', 'created_at', 'replies']

    def get_author(self, obj):
        post = self.context.get('post')
        return _author_data(obj, post)

    def get_replies(self, obj):
        return ReplySerializer(
            obj.replies.select_related('author').all(),
            many=True,
            context=self.context,
        ).data


def _serialize_comments(post):
    top_level = (
        post.comments
        .filter(parent=None)
        .select_related('author')
        .prefetch_related('replies__author')
    )
    return CommentSerializer(top_level, many=True, context={'post': post}).data


# ──────────────────────────────────────────
# TIP 게시글
# ──────────────────────────────────────────

class TipListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    has_images = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'category', 'like_count', 'comment_count', 'has_images', 'created_at']

    def get_author(self, obj):
        return _author_data(obj, obj)

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_has_images(self, obj):
        return obj.images.exists()


class TipDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'body', 'category', 'place',
            'is_anonymous', 'like_count', 'is_liked', 'images', 'comments', 'created_at',
        ]

    def get_author(self, obj):
        return _author_data(obj, obj)

    def get_place(self, obj):
        if not obj.place:
            return None
        return {
            "id": str(obj.place.id),
            "title": obj.place.title,
            "latitude": obj.place.latitude,
            "longitude": obj.place.longitude,
            "naver_map_url": obj.place.naver_map_url,
        }

    def get_comments(self, obj):
        return _serialize_comments(obj)

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(user=request.user).exists()


class TipCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()
    category = serializers.ChoiceField(choices=Post.TIP_CATEGORY_CHOICES)
    is_anonymous = serializers.BooleanField(default=False)
    place_id = serializers.UUIDField(required=False, allow_null=True, default=None)
    image_urls = serializers.ListField(
        child=serializers.URLField(), required=False, default=list
    )


# ──────────────────────────────────────────
# MAJOR 게시글
# ──────────────────────────────────────────

class MajorPostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    majors = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'majors', 'like_count', 'comment_count', 'created_at']

    def get_author(self, obj):
        return _author_data(obj, obj)

    def get_majors(self, obj):
        return list(obj.major_tags.select_related('major').values_list('major__major', flat=True))

    def get_comment_count(self, obj):
        return obj.comments.count()


class MajorPostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    majors = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'body', 'majors',
            'is_anonymous', 'like_count', 'is_liked', 'images', 'comments', 'created_at',
        ]

    def get_author(self, obj):
        return _author_data(obj, obj)

    def get_majors(self, obj):
        return [
            {"id": str(mt.major.id), "name": mt.major.major}
            for mt in obj.major_tags.select_related('major')
        ]

    def get_comments(self, obj):
        return _serialize_comments(obj)

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(user=request.user).exists()


class MajorPostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()
    major_ids = serializers.ListField(child=serializers.UUIDField(), min_length=1)
    is_anonymous = serializers.BooleanField(default=False)
    image_urls = serializers.ListField(
        child=serializers.URLField(), required=False, default=list
    )


# ──────────────────────────────────────────
# Comment 작성
# ──────────────────────────────────────────

class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField()
    is_anonymous = serializers.BooleanField(default=False)
