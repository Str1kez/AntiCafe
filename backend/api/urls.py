from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, RegisterAPIView


router = routers.DefaultRouter()
router.register('users', UserViewSet)


# TODO: СДЕЛАТЬ НЕ ТОЛЬКО POST ДЛЯ РЕГИСТРАЦИИ
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
