from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
# Local
from .yasg import urlpatterns as swa_urls

# router = routers.SimpleRouter()
# router.register(r'')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/', include('auths.urls')),
]

urlpatterns += swa_urls
