# Django
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import(
    IsAuthenticated, AllowAny
)

# Local
from .models import(
    CustomUser,  Invitation,
    Invitation, Tutor, Student
)
from .serializer import(
    CustomUserRegistrationSerializer,
    InvitationSerializer
)


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(
            email = email, 
            password = password
        )

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "error": "Неверные учетные данные."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


class InvitationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"])
    def send_invitation(self, request):
        serializer = InvitationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = request.user
        email = serializer.validated_data["email"]
        role = serializer.validated_data["role"]

        if user.is_superuser and role != "tutor":
            return Response(
                {"error": "Admins can only invite TUTORS!"}, status=400
            )

        if not user.is_superuser and role != "student":
            return Response(
                {"error": "Tutors can only invite STUDENTS!"}, status=400
            )
        
        invitation = Invitation.objects.create(
            email=email,
            inviter=user,
            role=role,
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            position_or_group=serializer.validated_data.get("position_or_group"),
        )

        registration_link = f"http://localhost:8080/register/{invitation.token}/"

        send_mail(
            "You're invited to our platform CODEVARS!!!!",
            f"Click the link to register: {registration_link} :)))",
            "noreply@platform.com",
            [email],
            fail_silently=False,
        )

        return Response(
            {"message": "Invitation sent successfully."},
            status=200
        )


class RegistrationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"], url_path="register")
    def register_with_invitation(self, request, pk=None):
        invitation = get_object_or_404(Invitation, token=pk)

        if invitation.is_used:
            return Response(
                {"error": "Invitation has already been used."},
                status=status.HTTP_400_BAD_REQUEST
            )

        password = request.data.get("password")
        if not password:
            return Response(
                {"error": "Password is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.create(
            email=invitation.email,
            first_name=invitation.first_name,
            last_name=invitation.last_name,
            role=invitation.role
        )
        user.set_password(password)
        user.save()

        if invitation.role == "tutor":
            Tutor.objects.create(
                user=user, 
                position=invitation.position_or_group
            )
        elif invitation.role == "student":
            Student.objects.create(
                user=user, 
                group=invitation.position_or_group
            )
        else:
            return Response(
                {"error": "Invalid role specified in the invitation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        invitation.is_used = True
        invitation.save()

        return Response(
            {"message": "Registration successful."},
            status=status.HTTP_201_CREATED
        )

