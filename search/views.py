from django.db.models import Q
from rest_framework.generics import ListAPIView

from accounts.models import User
from accounts.serializers import UserSerializer
from events.models import Event
from events.serializers import EventSerializer


# Create your views here.
class EventSearchView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        sport = self.request.query_params.get('sport', None)
        level = self.request.query_params.get('level', None)
        age_group = self.request.query_params.get('age_group', None)
        start_time = self.request.query_params.get('start_time', None)

        events = Event.objects.all()
        if title:
            events = events.filter(Q(title__icontains=title) |
                                   Q(description__icontains=title))
        if sport:
            events = events.filter(sport__name__icontains=sport)
        if level:
            events = events.filter(level__icontains=level)
        if age_group:
            events = events.filter(age_group__icontains=age_group)
        if start_time:
            events = events.filter(start_time__gte=start_time)
        return events


class UserSearchView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        param = self.request.query_params.get('param', None)

        return User.objects.filter(Q(username__icontains=param) |
                                   Q(name__icontains=param) |
                                   Q(email__icontains=param))
