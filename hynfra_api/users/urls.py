from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("user", UserViewSet, basename="users")

urlpatterns = [
    path(r"register/", RegisterView.as_view(), name="register"),
    path(r'guest-login/',guest_login,name="guest-login"),
    path(r'github-login/',github_sso_login,name="github-login"),
]

urlpatterns += router.urls


urlpatterns += [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
