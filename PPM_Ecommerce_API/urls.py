from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from ecommerce_products.views import ProductViewSet, ProductInventoryViewSet, ProductCategoryViewSet, DiscountViewSet
from ecommerce_users.views import UserViewSet
from core import views as core_views

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'productsinventory', ProductInventoryViewSet, basename='productsinventory')
router.register(r'productscategory', ProductCategoryViewSet, basename='productscategory')
router.register(r'discount', DiscountViewSet, basename='discount')
# router.register(r'order', ecommerce_views.OrderViewSet, basename='order') todo
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', core_views.ContactAPIView.as_view()),
    path('api-token-auth/', obtain_auth_token),  # access to token auth
]

urlpatterns += router.urls
