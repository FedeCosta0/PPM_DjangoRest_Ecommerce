from json import JSONDecodeError

from django.http import JsonResponse
from rest_framework import viewsets, status
from knox.auth import TokenAuthentication
from knox import views as knox_views
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from ecommerce_users.models import CustomUser
from .permissions import UserPermission
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer


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

            serializer = UserRegistrationSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                print(serializer.validated_data)
                print(repr(serializer.validated_data))
                validated_data = serializer.validated_data
                user = CustomUser.objects.create(email=validated_data['email'], password=validated_data['password'],
                                                 first_name=validated_data['first_name'], last_name=validated_data['last_name'])
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error", "message": "Json decoding error"}, status=400)


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



