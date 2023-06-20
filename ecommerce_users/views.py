from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from knox import views as knox_views
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from rest_framework.response import Response

from ecommerce_users.models import CustomUser
from .permissions import UserPermission
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer


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


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)

        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response.data, status=status.HTTP_200_OK)



