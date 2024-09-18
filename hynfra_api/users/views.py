from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,action
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets,generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import *
from .permissions import *
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # def get_permissions(self):
    #     if self.action in ['list', 'create', 'destroy']:
    #         self.permission_classes = [IsAuthenticated, IsAdmin]
    #     elif self.action in ['retrieve', 'update', 'partial_update']:
    #         self.permission_classes = [IsAuthenticated, IsStandardUser | IsAdmin]
    #     else:
    #         self.permission_classes = [IsAuthenticated, IsGuest]
    #     return super().get_permissions()
    
    @action(detail=False, methods=["GET"],permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def guest_login(request):
    """
    Allows user to login as guest
    """

    user_qs = User.objects.filter(
        role = "guest"
    )
    if not user_qs.exists():
        user = User.objects.create(
            username = "guest",
            email = "guest@gmail.com",
            role = "guest",
        )
        user.set_unusable_password()
        user.save()
    else:
        user = user_qs.first()
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
    

@api_view(["POST"])
@permission_classes([AllowAny])
def sso_login(request):
    """
    Github SSO Login
    """

    
