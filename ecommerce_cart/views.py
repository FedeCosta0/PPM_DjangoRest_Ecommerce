from decimal import Decimal
from json import JSONDecodeError

from django.http import JsonResponse
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from ecommerce_cart.models import Cart, CartProduct
from ecommerce_cart.permissions import CartProductPermission
from ecommerce_cart.serializers import CartSerializer, CartProductSerializer, CartProductCreationSerializer
from ecommerce_orders.models import OrderProduct, Order
from ecommerce_orders.serializers import OrderSerializer
from ecommerce_products.models import Product


class CartAPIViewSet(viewsets.GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = (CartProductPermission,)

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def retrieve(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(instance=cart)
        return Response(data=serializer.data)

    @action(detail=True, methods=['post'])
    def submit_order(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_products = CartProduct.objects.filter(cart=cart)
        if not cart_products.exists():
            return JsonResponse({"result": "error", "message": f"Empty cart"},
                                status=400)
        order = Order.objects.create(user=request.user, total=cart.total)

        for cart_product in cart_products:
            if not cart_product.is_available():
                return JsonResponse({"result": "error", "message": f"Not enough stock of {cart_product.product.name}"},
                                    status=400)
        for cart_product in cart_products:
            cart_product.reduce_stock_from_inventory()
            OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)
        cart.delete()
        Cart.objects.create(user=request.user)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class CartProductViewSet(DestroyModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (CartProductPermission,)
    serializer_class = CartProductSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        current_cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartProduct.objects.filter(cart=current_cart)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = CartProductCreationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                product = serializer.validated_data['product']
                quantity = serializer.validated_data['quantity']
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart.total += product.price * Decimal.from_float(float(quantity))
                cart.save()
                cart_product = CartProduct.objects.create(cart=cart, product=product,
                                                          quantity=quantity)
                return Response(CartProductSerializer(cart_product).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)

    def update(self, request, pk):
        try:
            print(pk)
            product = Product.objects.get(id=pk)
            data = JSONParser().parse(request)
            data['product'] = product.id
            serializer = CartProductCreationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                quantity = serializer.validated_data['quantity']
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart.total += product.price * Decimal.from_float(float(quantity))
                cart_product = CartProduct.objects.filter(cart=cart).get(product=product)
                cart_product.quantity += quantity
                cart_product.save()
                cart.save()
                return Response(CartProductSerializer(cart_product).data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cart = Cart.objects.get(user=request.user)
        cart.total -= instance.product.price * Decimal.from_float(float(instance.quantity))
        cart.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
