from django.urls import path
from .views import UpdateProfileView, ProfileView


urlpatterns = [
    path('editprofile/', UpdateProfileView.as_view(), name='edit_profile'),
    path('<int:id>', ProfileView.as_view(), name='profile_view'),
]
