from django.urls import path
from .views import EditProfileView, ProfileView

urlpatterns = [
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
]
