from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenBlacklistView

from .models import QRCode, User
from .schema.responses import (EMPTY_TOKEN_401, INVALID_TOKEN_401,
                               NO_PERMISSION_403, NOT_FOUND_404,
                               PAYMENT_REQUIRED_402, USER_EXISTS_400)
from .serializers import (QRCodeGenerationSerializer, QRCodeScanSerializer,
                          UserSerializer)


class AdminViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    # Вьюшка для админов кафешки
    """

    queryset = User.objects.filter(is_active=True, is_staff=False)
    # TODO: Нужен новый сериализатор для админа, чтобы не видеть/управлять личной инфой клиентов
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        tags=['admin'],
        operation_id='Client List',
        responses={
            200: UserSerializer(many=True),
            401: OpenApiTypes.OBJECT,
            403: OpenApiTypes.OBJECT,
        },
        examples=[
            INVALID_TOKEN_401,
            EMPTY_TOKEN_401,
            NO_PERMISSION_403,
        ],
    )
    def list(self, request, *args, **kwargs):
        """
        # Получение списка клиентов
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['admin'],
        operation_id='Client Retrieve',
        parameters=[
            OpenApiParameter(
                'id',
                OpenApiTypes.UUID,
                'path',
                required=True,
                description='ID Клиента',
                examples=[OpenApiExample('id_example', '3fa85f64-5717-4562-b3fc-2c963f66afa6')],
            )
        ],
        responses={
            200: UserSerializer,
            401: OpenApiTypes.OBJECT,
            403: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            INVALID_TOKEN_401,
            EMPTY_TOKEN_401,
            NO_PERMISSION_403,
            NOT_FOUND_404,
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        """
        # Получение инфы об определенном клиенте
        """
        return super().retrieve(request, *args, **kwargs)


class UserViewSet(viewsets.GenericViewSet):
    """
    # Вьюшка для авторизированных клиентов
    """

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['client'],
        operation_id='Client Info',
        responses={
            200: UserSerializer,
            401: OpenApiTypes.OBJECT,
        },
        examples=[
            INVALID_TOKEN_401,
            EMPTY_TOKEN_401,
        ],
    )
    @action(detail=False, url_path='client', url_name='user_info')
    def info(self, request, *args, **kwargs):
        """
        # Получение инфы о себе
        """
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @extend_schema(
        tags=['client'],
        operation_id='Client',
        responses={
            204: None,
            401: OpenApiTypes.OBJECT,
        },
        examples=[
            INVALID_TOKEN_401,
            EMPTY_TOKEN_401,
        ],
    )
    @info.mapping.delete
    def delete(self, request, *args, **kwargs):
        """
        # Удаление пользователя
        ## Вместо удаления отмечаем их как не активные
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        tags=['client'],
        operation_id='Client Bio',
        responses={
            200: UserSerializer,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
        },
        examples=[
            USER_EXISTS_400,
            INVALID_TOKEN_401,
            EMPTY_TOKEN_401,
        ],
    )
    @info.mapping.patch
    def update_bio(self, request, *args, **kwargs):
        """
        # Обновление ***о себе***
        ## Юзаем `PATCH` запрос, чтобы не удалить пустые поля
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self) -> User:
        return self.request.user


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    # Вьюшка для регистрации
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id='User',
        auth=[],
        responses={
            200: UserSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            USER_EXISTS_400,
        ],
    )
    def create(self, request, *args, **kwargs):
        """
        # Регистрация пользователя
        """
        response = super().create(request, *args, **kwargs)
        return Response(status=response.status_code, headers=response.headers)


class CustomTokenBlacklistView(TokenBlacklistView):
    """
    # Need to be authenticated for logout
    Front must go to endpoint with `'refresh'` token in data
    After that, delete `'access'` token from cookie
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class QRCodeGenerateViewSet(viewsets.GenericViewSet):
    serializer_class = QRCodeGenerationSerializer
    permission_classes = [IsAuthenticated]
    queryset = QRCode.objects.filter(closed=False)

    @extend_schema(
        operation_id='Generate QRCode',
        request=None,
        responses={
            200: QRCodeGenerationSerializer,
            401: OpenApiTypes.OBJECT,
            402: OpenApiTypes.OBJECT,
        },
        examples=[
            INVALID_TOKEN_401,
            EMPTY_TOKEN_401,
            PAYMENT_REQUIRED_402,
        ],
    )
    def create(self, request, *args, **kwargs):
        """
        # Генерация QR-кода
        """
        user = self.get_object()
        opened_bill = user.qrcodes.filter(closed=False).exists()
        if opened_bill:
            return Response(
                {'detail': 'Есть неоплаченный счет'},
                status=status.HTTP_402_PAYMENT_REQUIRED,
                content_type='application/json',
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        return self.request.user


class QRCodeScanViewSet(viewsets.GenericViewSet):
    serializer_class = QRCodeScanSerializer
    permission_classes = [IsAdminUser]
    queryset = QRCode.objects.filter(closed=False)

    @extend_schema(
        operation_id='Scan QRCode',
        request=None,
        parameters=[
            OpenApiParameter(
                'id',
                OpenApiTypes.UUID,
                'path',
                required=True,
                description='ID QRCode',
                examples=[OpenApiExample('id_example', '3fa85f64-5717-4562-b3fc-2c963f66afa6')],
            )
        ],
        responses={
            200: QRCodeScanSerializer,
            401: OpenApiTypes.OBJECT,
            403: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
        examples=[
            INVALID_TOKEN_401,
            EMPTY_TOKEN_401,
            NO_PERMISSION_403,
            NOT_FOUND_404,
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        """
        # Обновляет код как **оплаченный**
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
