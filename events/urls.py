from django.urls import path
from .views import EventCreateView, EventListView, EventOneView, EventQuitView, \
    EventUpdateView, EventJoinView

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='event-list'),
    path('<int:id>/', EventOneView.as_view(), name='event-one'),
    path('update/', EventUpdateView.as_view(), name='event-update'),
    path('join/', EventJoinView.as_view(), name='event-join'),
    path('quit/', EventQuitView.as_view(), name='event-quit'),
]
