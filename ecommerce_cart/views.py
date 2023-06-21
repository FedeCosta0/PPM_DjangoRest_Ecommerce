from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import viewsets, status
from knox.auth import TokenAuthentication
from rest_framework import views
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ecommerce_cart.models import ShoppingSession, CartProduct
from ecommerce_cart.permissions import ShoppingSessionPermission, CartProductPermission
from ecommerce_cart.serializers import ShoppingSessionSerializer, CartProductSerializer, CartProductCreationSerializer
from ecommerce_products.models import Product


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


class CartAPIView(views.APIView):
    serializer_class = ShoppingSessionSerializer

    def get(self, request):
        cart, created = ShoppingSession.objects.get_or_create(user=request.user)
        serializer = ShoppingSessionSerializer(instance=cart)
        print(repr(serializer.data))
        print(repr(serializer))
        return Response(data=serializer.data)


class CartProductViewSet(RetrieveModelMixin, ListModelMixin, DestroyModelMixin, UpdateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
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
                product_id = serializer.validated_data['product']
                quantity = serializer.validated_data['quantity']
                product = Product.objects.get(id=product_id)
                shopping_session, created = ShoppingSession.objects.get_or_create(user=request.user)
                shopping_session.total += product.price * quantity
                shopping_session.save()
                cart_product = CartProduct.objects.create(shopping_session=shopping_session, product=product,
                                                          quantity=quantity)
                return Response(CartProductSerializer(cart_product).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)

