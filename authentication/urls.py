# myapp/urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('login/', login_view(), name='login'),
    path('login/', TokenObtainPairView.as_view()),
    path('apil/token/refresh/', TokenRefreshView.as_view()),
    # Add more URLs as needed
]
