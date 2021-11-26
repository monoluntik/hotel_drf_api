from django.urls import path, include
from .views import ActivateView, RegisterView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:activation_code>/', ActivateView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view()),
]