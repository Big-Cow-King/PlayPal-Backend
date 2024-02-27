from django.urls import path
from .views import NotificationListAPIView, NotificationReadAPIView

urlpatterns = [
    path('list/', NotificationListAPIView.as_view(), name='notifications-list'),
    path('read/', NotificationReadAPIView.as_view(), name='notifications-read'),
]
