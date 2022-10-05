from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenBlacklistView

from .models import User
from .serializers import UserSerializer


class AdminViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    """
    Viewset for cafe admins
    """
    queryset = User.objects.filter(is_active=True, is_staff=False)
    # TODO: Нужен новый сериализатор для админа, чтобы не видеть/управлять личной инфой клиентов
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserViewSet(viewsets.GenericViewSet):
    """
    Viewset for clients
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, url_path='client', url_name='user_info')
    def info(self, request, *args, **kwargs):
        """
        Get user info
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @info.mapping.delete
    def delete(self, request, *args, **kwargs):
        """
        Marking Users as inactive instead of deleting
        Front must go to /token/blacklist/ endpoint with 'refresh' token in data
        After that, delete 'access' token from cookie
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @info.mapping.patch
    def update_bio(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self) -> User:
        return self.request.user


class RegisterViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    """
    Simple View for registration
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Register user -> 201 code
        """
        response = super().create(request, *args, **kwargs)
        return Response(status=response.status_code, headers=response.headers)


class CustomTokenBlacklistView(TokenBlacklistView):
    """
    Need to be authenticated for logout
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
