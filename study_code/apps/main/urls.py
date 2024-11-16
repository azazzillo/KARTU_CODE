# Django
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
# Local
from .views import RegistrationViewSet

# router = routers.SimpleRouter()
# router.register(r'')

urlpatterns = [
    path('sign-in/', RegistrationViewSet.as_view({'post':'create'}), name='registration'),
]
