from rest_framework import serializers
from .models import CustomUser

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(min_length=8)
    password2 = serializers.CharField(min_length=8)

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 존재하는 아이디입니다.")
        return value

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError("두 비밀번호가 일치하지 않습니다.")
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
        )