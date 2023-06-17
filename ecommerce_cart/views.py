from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from ecommerce_cart.models import ShoppingSession, CartProduct
from ecommerce_cart.permissions import ShoppingSessionPermission
from ecommerce_cart.serializers import ShoppingSessionSerializer, CartProductSerializer


# Create your views here.


class ShoppingSessionViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = (ShoppingSessionPermission,)
    serializer_class = ShoppingSessionSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        return ShoppingSession.objects.filter(user=user)

    def create(self, request):
        user = request.user
        total = 0.00
        shopping_session = ShoppingSession.objects.create(user=user, total=total)
        return Response(ShoppingSessionSerializer(shopping_session).data)


class CartProductViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, UpdateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (ShoppingSessionPermission,)
    serializer_class = CartProductSerializer
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user = self.request.user
        return CartProduct.objects.filter(user=user)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            shopping_session = ShoppingSession.objects.get_or_create(user=request.user)
            product = data['product']
            quantity = data['quantity']
            cart_product = CartProduct.objects.create(shopping_session=shopping_session, product=product,
                                                      quantity=quantity)
            return Response(CartProductSerializer(cart_product.data))

        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)