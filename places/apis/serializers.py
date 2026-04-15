from rest_framework import serializers

from places.models import Place


def _author_data(obj):
    """Place 작성자 정보 반환. 익명이면 null."""
    if obj.author is None or obj.is_anonymous:
        return None
    return {
        "grade": obj.author.grade,
        "class_num": obj.author.class_num,
        "num": obj.author.num,
        "name": obj.author.name,
    }


class PlaceSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = [
            'id', 'author', 'title', 'description', 'category',
            'latitude', 'longitude', 'naver_map_url', 'is_anonymous', 'created_at',
        ]

    def get_author(self, obj):
        return _author_data(obj)


class PlaceCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    category = serializers.ChoiceField(choices=Place.CATEGORY_CHOICES)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    naver_map_url = serializers.URLField(required=False, allow_blank=True, default=None)
    is_anonymous = serializers.BooleanField(default=False)
