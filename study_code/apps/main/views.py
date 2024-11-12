# Django
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import(
    IsAuthenticated,
)

# Local
from apps.auth.models import(
    CustomUser, 
)
from serializer import(
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    model = CustomUser
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = [IsAuthenticated]

