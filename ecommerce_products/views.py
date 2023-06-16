from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from .permissions import ProductPermission, ProductCategoryPermission, ProductInventoryPermission, DiscountPermission
from .models import Product, ProductCategory, ProductInventory, Discount
from .serializers import ProductSerializer, ProductCreationSerializer, ProductCategorySerializer, ProductInventorySerializer, DiscountSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ProductPermission,)
    serializer_class = ProductSerializer

    serializer_action_classes = {
        'list': ProductSerializer,
        'retrieve': ProductSerializer,
        'create': ProductCreationSerializer,
    }


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
