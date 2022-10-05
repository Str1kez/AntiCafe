from rest_framework import viewsets, status, mixins
# from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


# class RegisterAPIView(CreateAPIView):
#     # TODO: Написать для регистрации с set_password
#     model = User
#     serializer_class = UserSerializer


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    """
    Simple model view set (testing)
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # TODO: ОПИСАТЬ РЕГУ С РЕДИРЕКТОМ НА ТОКЕН
    # def create(self, request, *args, **kwargs):
    #     pass

    def get_permissions(self):
        """
        Permission for every action
        """
        match self.action:
            case 'create':
                permission_classes = []
            # TODO: Изменить права для удаления своего аккаунта
            case 'destroy' | 'list':
                permission_classes = [IsAdminUser]
            case 'retrieve' | 'partial_update':
                permission_classes = [IsAuthenticated]
            case _:
                permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
