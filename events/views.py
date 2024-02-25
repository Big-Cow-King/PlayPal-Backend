from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, \
    UpdateAPIView, DestroyAPIView
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
        return get_object_or_404(Event, id=self.kwargs.get('id'))


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
        event = get_object_or_404(Event, id=request.data.get('id'))
        user = request.user
        if user in event.players.all():
            return JsonResponse({'message': 'You are already in this event'}, status=400)
        event.players.add(user)
        event.save()
        return JsonResponse({'message': 'Joined event successfully!'}, status=200)


class EventDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_object(self):
        eid = self.request.data.get('id')
        return get_object_or_404(Event, id=eid, owner=self.request.user)


class EventQuitView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_object(self):
        eid = self.request.data.get('id')
        return get_object_or_404(Event, id=eid)

    def update(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=request.data.get('id'))
        user = request.user
        if user not in event.players.all():
            return JsonResponse({'message': 'You are not in this event'}, status=400)
        event.players.remove(user)
        event.save()
        return JsonResponse({'message': 'Left event successfully!'}, status=200)
