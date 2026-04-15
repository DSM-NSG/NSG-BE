from rest_framework import serializers


class UserTestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class LoginSerializer(serializers.Serializer):
    grade = serializers.IntegerField(min_value=1, max_value=3)
    class_num = serializers.IntegerField(min_value=1)
    num = serializers.IntegerField(min_value=1)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
