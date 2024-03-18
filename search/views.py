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
        keywords = self.request.query_params.get('keywords', None)
        sports = self.request.query_params.getlist('sports', None)
        levels = self.request.query_params.getlist('levels', None)
        age_groups = self.request.query_params.getlist('age_groups', None)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)

        events = Event.objects.all().filter(visibility='Public')
        if keywords:
            events = events.filter(Q(title__icontains=keywords) |
                                   Q(description__icontains=keywords) |
                                   Q(content__icontains=keywords))
        if sports:
            events = events.filter(sport__in=sports)
        if levels:
            events = events.filter(level__in=levels)
        if age_groups:
            events = events.filter(age_group__in=age_groups)
        if start_time:
            events = events.filter(start_time__gte=start_time)
        if end_time:
            events = events.filter(end_time__lte=end_time)

        return events


class UserSearchView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        param = self.request.query_params.get('param', None)

        return User.objects.filter(Q(username__icontains=param) |
                                   Q(name__icontains=param) |
                                   Q(email__icontains=param))
