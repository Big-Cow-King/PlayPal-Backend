from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.detail_serializers import UserDetailSerializer


# Create your views here.
class SignUpView(CreateAPIView):
    serializer_class = UserSerializer


class UserView(RetrieveAPIView):
    serializer_class = UserDetailSerializer

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs.get('id'))


class UserUpdateView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
