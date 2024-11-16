# Django
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import(
    IsAuthenticated,
)

# Local
from auths.models import CustomUser
from .serializer import(
    CustomUserRegistrationSerializer
)


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    pagination_class = [IsAuthenticated]
    
    def create(self, request):
        serializer = self.serializer_class
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 
                    f"User {serializer.data['first_name']} registrated successfully"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


