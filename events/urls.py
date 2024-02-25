from django.urls import path
from .views import EventCreateView, EventDeleteView, EventListView, \
    EventOneView, EventQuitView,  EventUpdateView, EventJoinView, \
    NotificationListView


urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='event-list'),
    path('<int:id>/', EventOneView.as_view(), name='event-one'),
    path('update/', EventUpdateView.as_view(), name='event-update'),
    path('join/', EventJoinView.as_view(), name='event-join'),
    path('delete/', EventDeleteView.as_view(), name='event-delete'),
    path('quit/', EventQuitView.as_view(), name='event-quit'),
    path('notifications/<int:playerid>/', NotificationListView.as_view(), name='notification-list'),
]
