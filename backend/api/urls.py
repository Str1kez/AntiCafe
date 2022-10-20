from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserViewSet,
    RegisterViewSet,
    CustomTokenBlacklistView,
    AdminViewSet,
)

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='')
router.register('admin', AdminViewSet)
router.register('register', RegisterViewSet)


urlpatterns = [
    path('users/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'token/blacklist/',
        CustomTokenBlacklistView.as_view(),
        name='token_blacklist',
    ),
]
