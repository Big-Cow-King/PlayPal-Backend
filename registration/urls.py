# yourappname/urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', SignUpView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('apil/token/refresh/', TokenRefreshView.as_view()),
]
