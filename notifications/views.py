from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from notifications.models import Notification
from .serializers import NotificationSerializer


# Create your views here.
class NotificationListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(player_id=self.request.user)


class NotificationReadAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_object(self):
        return get_object_or_404(Notification, id=self.request.data.get('id'), player_id=self.request.user)
