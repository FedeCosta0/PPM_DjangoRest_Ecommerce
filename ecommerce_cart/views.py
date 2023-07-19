from decimal import Decimal
from json import JSONDecodeError

from django.http import JsonResponse
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from ecommerce_cart.models import ShoppingSession, CartProduct
from ecommerce_cart.permissions import CartProductPermission
from ecommerce_cart.serializers import ShoppingSessionSerializer, CartProductSerializer, CartProductCreationSerializer
from ecommerce_orders.models import OrderProduct, Order
from ecommerce_orders.serializers import OrderSerializer


class CartAPIView(viewsets.GenericViewSet):
    serializer_class = ShoppingSessionSerializer
    permission_classes = (CartProductPermission,)

    def get_queryset(self):
        user = self.request.user
        return ShoppingSession.objects.filter(user=user)

    def retrieve(self, request):
        cart, created = ShoppingSession.objects.get_or_create(user=request.user)
        serializer = ShoppingSessionSerializer(instance=cart)
        return Response(data=serializer.data)

    @action(detail=True, methods=['post'])
    def submit_order(self, request):
        shopping_session = ShoppingSession.objects.get(user=request.user)
        cart_products = CartProduct.objects.filter(shopping_session=shopping_session)
        if not cart_products.exists():
            return JsonResponse({"result": "error", "message": f"Empty cart"},
                                status=400)
        order = Order.objects.create(user=request.user, total=shopping_session.total)

        for cart_product in cart_products:
            if not cart_product.is_available():
                return JsonResponse({"result": "error", "message": f"Not enough stock of {cart_product.product.name}"},
                                    status=400)
        for cart_product in cart_products:
            cart_product.reduce_stock_from_inventory()
            OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)
        shopping_session.delete()
        ShoppingSession.objects.create(user=request.user)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class CartProductViewSet(DestroyModelMixin, UpdateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (CartProductPermission,)
    serializer_class = CartProductSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        current_shopping_session, created = ShoppingSession.objects.get_or_create(user=self.request.user)
        return CartProduct.objects.filter(shopping_session=current_shopping_session)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = CartProductCreationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                product = serializer.validated_data['product']
                quantity = serializer.validated_data['quantity']
                shopping_session, created = ShoppingSession.objects.get_or_create(user=request.user)
                shopping_session.total += product.price * Decimal.from_float(float(quantity))
                shopping_session.save()
                cart_product = CartProduct.objects.create(shopping_session=shopping_session, product=product,
                                                          quantity=quantity)
                return Response(CartProductSerializer(cart_product).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        shopping_session = ShoppingSession.objects.get(user=request.user)
        shopping_session.total -= instance.product.price * Decimal.from_float(float(instance.quantity))
        shopping_session.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
