from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet for listing or retrieving products.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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
