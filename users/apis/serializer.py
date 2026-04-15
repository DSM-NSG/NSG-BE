from rest_framework import serializers


class UserTestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class LoginSerializer(serializers.Serializer):
    account_id = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class UserInfoSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    account_id = serializers.CharField()
    name = serializers.CharField()
    grade = serializers.IntegerField()
    class_num = serializers.IntegerField()
    num = serializers.IntegerField()


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserInfoSerializer()
