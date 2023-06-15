from django.urls import path
from .views import UserViewSet
urlpatterns = [
  path("get-detail", UserDetailAPI.as_view()),
  path('register', RegisterUserAPIView.as_view()),
]