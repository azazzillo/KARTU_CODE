from rest_framework import serializers
from auths.models import CustomUser


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )

    def create(self, validated_data):

        user = CustomUser.objects.create(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'firstname', 'lastname', 'password',
        )
        write_only_fields = ('password',)
        read_only_fields = ('id',)

