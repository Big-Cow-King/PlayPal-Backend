from django.urls import path

from feedbacks.views import FeedbackCreateView, FeedbackDeleteView, \
    FeedbackListView, \
    FeedbackOneView, FeedbackUpdateView

urlpatterns = [
    path('create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('list/<int:eid>/', FeedbackListView.as_view(), name='feedback-list'),
    path('<int:eid>/', FeedbackOneView.as_view(), name='feedback-one'),
    path('update/', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('delete/', FeedbackDeleteView.as_view(), name='feedback-delete'),
]
