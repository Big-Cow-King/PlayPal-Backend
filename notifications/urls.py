from django.urls import path
from .views import NotificationListAPIView


urlpatterns = [
    path('list/', NotificationListAPIView.as_view(), name='notifications-list'),
]
