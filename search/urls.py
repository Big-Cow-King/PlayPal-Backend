from django.urls import path

from search.views import EventSearchView

urlpatterns = [
    path('events/', EventSearchView.as_view(), name='event_search'),
]
