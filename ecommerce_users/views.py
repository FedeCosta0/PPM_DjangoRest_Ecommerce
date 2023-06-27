from json import JSONDecodeError

from django.contrib.auth import login
from django.http import JsonResponse
from knox import views as knox_views
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ecommerce_users.models import CustomUser, UserAddress
from .permissions import UserPermission, UserAddressPermission
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer, UserAddressSerializer


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserPermission,)
    serializer_class = UserSerializer

    serializer_action_classes = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'update': UserSerializer,
        'create': UserRegistrationSerializer,
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
                user = serializer.create(validated_data=validated_data)
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


class LoginAPIView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        try:
            data = JSONParser().parse(request)
            serializer = self.serializer_class(data=data)

            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                login(request, user)
                response = super().post(request, format=None)
                return Response(response.data, status=status.HTTP_200_OK)
            else:
                return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


class UserAddressViewSet(RetrieveModelMixin, UpdateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UserAddressPermission,)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return UserAddress.objects.all()
        else:
            return UserAddress.objects.filter(user=user)

    def create(self, request):
        try:
            data = JSONParser().parse(request)
            data['user'] = request.user.id
            serializer = self.serializer_class(data=data)

            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                user_address = UserAddress.objects.create(user=validated_data['user'],
                                                          address=validated_data['address'],
                                                          city=validated_data['city'],
                                                          postal_code=validated_data['postal_code'],
                                                          country=validated_data['country'],
                                                          telephone=validated_data['telephone'])
                return Response(UserAddressSerializer(user_address).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)
