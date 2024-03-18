from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, \
    UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer


# Create your views here.
class FeedbackCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer


class FeedbackListView(ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.all().filter(event_id=self.kwargs.get('eid'))


class FeedbackOneView(RetrieveAPIView):
    serializer_class = FeedbackSerializer

    def get_object(self):
        eid = self.request.data.get('eid')
        return get_object_or_404(Feedback, event_id=eid, user=self.request.user)


class FeedbackUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def get_object(self):
        eid = self.request.data.get('eid')
        return get_object_or_404(Feedback, event_id=eid, user=self.request.user)


class FeedbackDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def get_object(self):
        eid = self.request.data.get('eid')
        return get_object_or_404(Feedback, event_id=eid, user=self.request.user)
