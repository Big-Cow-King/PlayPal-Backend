from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import SignUpView, UserView, UserUpdateView

urlpatterns = [
    path('register/', SignUpView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('editprofile/', UserUpdateView.as_view(), name='edit_profile'),
    path('<int:id>/', UserView.as_view(), name='profile_view'),
]
