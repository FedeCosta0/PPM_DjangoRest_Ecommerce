from json import JSONDecodeError

from django.http import JsonResponse
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, ProductCategory, ProductInventory, Discount
from .permissions import ProductPermission, ProductCategoryPermission, ProductInventoryPermission, DiscountPermission
from .serializers import ProductSerializer, ProductCreationSerializer, ProductCategorySerializer, \
    ProductInventorySerializer, DiscountSerializer


class ProductViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProductPermission,)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

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
            serializer = self.get_serializer_class()(data=data)
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                category = ProductCategory.objects.get(id=validated_data['category'].id)
                inventory_instance = ProductInventory.objects.create()
                discount_instance, created = Discount.objects.get_or_create(name="NullDiscount")
                product = Product.objects.create(name=validated_data['name'], description=validated_data['description'],
                                                 price=validated_data['price'],
                                                 category=category, inventory=inventory_instance,
                                                 discount=discount_instance)
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


class ProductCategoryViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = ProductCategory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProductCategoryPermission,)
    serializer_class = ProductCategorySerializer
    lookup_field = 'slug'

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                category = ProductCategory.objects.create(name=validated_data['name'],
                                                          description=validated_data['description'])
                return Response(ProductCategorySerializer(category).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


class ProductInventoryView(APIView):
    queryset = ProductInventory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProductInventoryPermission,)
    serializer_class = ProductInventorySerializer

    def put(self, request, slug):
        try:
            data = JSONParser().parse(request)
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                quantity = validated_data['stock']
                product = Product.objects.get(slug=slug)
                product_inventory = ProductInventory.objects.get(product=product)
                product_inventory.add_stock(quantity)
                product_inventory.save()
                return Response(ProductInventorySerializer(product_inventory).data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


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
