from django.contrib import admin
from django.urls import path
from rest_framework import routers
from knox.views import LogoutView, LogoutAllView

from ecommerce_products.views import ProductViewSet, ProductInventoryViewSet, ProductCategoryViewSet, DiscountViewSet
from ecommerce_users.views import UserViewSet, LoginAPIView
from ecommerce_cart.views import ShoppingSessionViewSet, CartProductViewSet, CartAPIView
from core import views as core_views

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'products-inventory', ProductInventoryViewSet, basename='productsinventory')
router.register(r'products-category', ProductCategoryViewSet, basename='productscategory')
router.register(r'discount', DiscountViewSet, basename='discount')
# router.register(r'cart', ShoppingSessionViewSet, basename='cart')
router.register(r'cart-product', CartProductViewSet, basename='cart-product')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', core_views.ContactAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('cart/', CartAPIView.as_view()),
]

urlpatterns += router.urls
