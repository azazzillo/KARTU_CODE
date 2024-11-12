from rest_framework import serializers
from apps.auth.models import CustomUser


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'first_name', 'last_name',
            'password'
        ]

