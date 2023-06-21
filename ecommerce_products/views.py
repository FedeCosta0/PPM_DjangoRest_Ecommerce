from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import viewsets, status
from knox.auth import TokenAuthentication
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Product, ProductCategory, ProductInventory, Discount
from .permissions import ProductPermission, ProductCategoryPermission, ProductInventoryPermission, DiscountPermission
from .serializers import ProductSerializer, ProductCreationSerializer, ProductCategorySerializer, \
    ProductInventorySerializer, DiscountSerializer


class ProductViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProductPermission,)
    serializer_class = ProductSerializer

    serializer_action_classes = {
        'list': ProductSerializer,
        'retrieve': ProductSerializer,
        'create': ProductCreationSerializer,
    }
    
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            print('data:')
            print(data)
            serializer = self.serializer_class(data=data)
            print('serializer:')
            print(repr(serializer))
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                print('validated_data:')
                print(validated_data)
                product = Product.objects.create(name=validated_data['name'], description=validated_data['description'],
                                                 price=validated_data['price'],
                                                 category=validated_data['category'])
                return Response(ProductCreationSerializer(product).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProductCategoryPermission,)
    serializer_class = ProductCategorySerializer


class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProductInventoryPermission,)
    serializer_class = ProductInventorySerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (DiscountPermission,)
    serializer_class = DiscountSerializer


"""
class OrderViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    viewsets.GenericViewSet
):

    ViewSet for listing, retrieving and creating orders.

    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):

        This view should return a list of all the orders
        for the currently authenticated user.

        user = self.request.user
        return Order.objects.filter(user=user)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = OrderSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                item = Product.objects.get(pk=data["item"])
                order = item.place_order(request.user, data["quantity"])
                return Response(OrderSerializer(order).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)
            
"""
