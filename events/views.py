from django.shortcuts import get_object_or_404, render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from events.models import Event
from events.serializers import EventSerializer


# Create your views here.
class EventCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer


class EventListView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.all()


class EventOneView(RetrieveAPIView):
    serializer_class = EventSerializer

    def get_object(self):
        return Event.objects.get(id=self.kwargs.get('id'))


class EventUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_object(self):
        eid = self.request.data.get('id')
        return get_object_or_404(Event, id=eid, owner=self.request.user)


class EventJoinView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_object(self):
        eid = self.request.data.get('id')
        return get_object_or_404(Event, id=eid)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        event.players.add(request.user)
        event.save()
        return event
