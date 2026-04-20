from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class ImageUploadResponseSerializer(serializers.Serializer):
    url = serializers.URLField()
