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

user_router = routers.DefaultRouter()
user_router.register('', UserViewSet, basename='')
user_router.register('admin', AdminViewSet)
user_router.register('register', RegisterViewSet)

# qrcode_router = routers.DefaultRouter()
# qrcode_router.register('generate', ...)
# qrcode_router.register('verify', ...)


urlpatterns = [
    # path('qrcode/', include(qrcode_router.urls)),
    path('users/', include(user_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'token/blacklist/',
        CustomTokenBlacklistView.as_view(),
        name='token_blacklist',
    ),
]
