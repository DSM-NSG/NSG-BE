from rest_framework import serializers


class UserTestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)


class LoginSerializer(serializers.Serializer):
    account_id = serializers.CharField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
