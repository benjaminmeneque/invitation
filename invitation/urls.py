from django.urls import path
from .views import CreateInvitationView, InvitationSuccess

urlpatterns = [
    path("", CreateInvitationView.as_view(), name="invitation"),
    path("invitation-success/", InvitationSuccess.as_view(), name="invitation_success"),
]
