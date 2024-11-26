from rest_framework import serializers

# Local
from .models import(
    CustomUser, Tutor, Student, Invitation
)


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
            'id', 'email', 'first_name', 'last_name', 'password',
        )
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class TutorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Tutor
        fields = ["first_name", "last_name", "password"]

    def create(self, validated_data):
        tutor = Tutor(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=self.context["email"],
        )
        tutor.set_password(validated_data["password"])
        tutor.save()
        return tutor


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "password", "group"]

    def create(self, validated_data):
        student = Student(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            group=validated_data["group"],
            email=self.context["email"],
        )
        student.set_password(validated_data["password"])
        student.save()
        return student


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["email", "role", "first_name", "last_name", "position_or_group"]