from django.urls import path

from search.views import EventSearchView, UserSearchView

urlpatterns = [
    path('events/', EventSearchView.as_view(), name='event_search'),
    path('users/', UserSearchView.as_view(), name='user_search'),
]
