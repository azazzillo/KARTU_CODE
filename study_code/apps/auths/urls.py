from django.urls import path

# Local
from .views import(
    LoginViewSet, InvitationViewSet,
    RegistrationViewSet
)


invitation_view = InvitationViewSet.as_view({
    'post': 'send_invitation',
})

registration_viewset = RegistrationViewSet.as_view({
    'post': 'register_with_invitation'
})


urlpatterns = [
    path("login/", LoginViewSet.as_view({"post": "create"}), name="login"),
    path('invitations/send/', invitation_view, name='send-invitation'),
    path('api/register/<str:pk>/', registration_viewset, name='register_with_invitation'),
]