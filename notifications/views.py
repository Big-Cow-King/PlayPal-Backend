from collections import OrderedDict

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from notifications.models import Notification
from .serializers import NotificationSerializer


class CountUnreadNotificationsPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('unread', Notification.objects.filter(player_id=self.request.user,
                                                   read=False).count()),
            ('results', data)
        ]))


# Create your views here.
class NotificationListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = CountUnreadNotificationsPagination

    def get_queryset(self):
        return Notification.objects.filter(
            player_id=self.request.user).order_by('-created_at')


class NotificationReadAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_object(self):
        return get_object_or_404(Notification, id=self.request.data.get('id'),
                                 player_id=self.request.user)


class NotificationDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_object(self):
        return get_object_or_404(Notification, id=self.request.data.get('id'),
                                 player_id=self.request.user)
