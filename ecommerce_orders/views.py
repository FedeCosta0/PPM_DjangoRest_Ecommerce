from knox.auth import TokenAuthentication
from rest_framework import viewsets
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from .models import Order
from .permissions import OrderPermission
from .serializers import OrderSerializer


class OrderViewSet(RetrieveModelMixin, ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (OrderPermission,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
