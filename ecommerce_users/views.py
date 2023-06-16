from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from ecommerce_users.models import CustomUser
from .permissions import UserPermission
from .serializers import UserSerializer, UserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserPermission,)
    serializer_class = UserSerializer

    serializer_action_classes = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'create': UserRegistrationSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
