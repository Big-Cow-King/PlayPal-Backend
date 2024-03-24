from django.urls import path
from notifications.views import NotificationDeleteView, NotificationListAPIView, \
    NotificationReadAPIView

urlpatterns = [
    path('list/', NotificationListAPIView.as_view(), name='notifications-list'),
    path('read/', NotificationReadAPIView.as_view(), name='notifications-read'),
    path('delete/', NotificationDeleteView.as_view(), name='notifications-delete'),
]
