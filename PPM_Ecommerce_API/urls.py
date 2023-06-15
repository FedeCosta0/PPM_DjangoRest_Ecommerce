from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from ecommerce_users.views import UserViewSet
from core import views as core_views

router = routers.DefaultRouter()
# router.register(r'item', ecommerce_views.ItemViewSet, basename='item')
# router.register(r'order', ecommerce_views.OrderViewSet, basename='order') todo
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', core_views.ContactAPIView.as_view()),
    path('api-token-auth/', obtain_auth_token),  # access to token auth
]

urlpatterns += router.urls
