from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from userprofile.serializers import ProfileSerializer
from userprofile.models import Profile


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        profile = Profile.objects.get_or_create(user=self.request.user)
        return profile


class UpdateProfileView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = get_object_or_404(User, id=self.request.user)
        return get_object_or_404(Profile, user=user)