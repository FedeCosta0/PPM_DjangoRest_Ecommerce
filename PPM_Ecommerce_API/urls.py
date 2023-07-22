from django.contrib import admin
from django.urls import path
from knox.views import LogoutView, LogoutAllView
from rest_framework import routers

from ecommerce_cart.views import CartProductViewSet, CartAPIView
from ecommerce_products.views import ProductViewSet, ProductInventoryViewSet, ProductCategoryViewSet, DiscountViewSet
from ecommerce_users.views import UserViewSet, LoginAPIView, UserAddressViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'products-inventory', ProductInventoryViewSet, basename='productsinventory')
router.register(r'products-category', ProductCategoryViewSet, basename='productscategory')
router.register(r'discount', DiscountViewSet, basename='discount')
router.register(r'cart-product', CartProductViewSet, basename='cart-product')
router.register(r'users', UserViewSet, basename='users')
router.register(r'addresses', UserAddressViewSet, basename='addresses')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    path('cart/', CartAPIView.as_view({'get': 'retrieve', 'post': 'submit_order'})),
]

urlpatterns += router.urls
