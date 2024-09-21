from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,action
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets,generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import *
from .permissions import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import requests
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
def github_sso_login(request):
    """
    Github SSO Login
    """
    code = request.data.get('code')
    if not code:
        return Response({'error': 'Code is required'}, status=400)

    token_url = 'https://github.com/login/oauth/access_token'
    headers = {'Accept': 'application/json'}
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.GITHUB_REDIRECT_URI,
    }

    # Exchange the authorization code for an access token
    token_response = requests.post(token_url, headers=headers, data=data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if access_token:
        user_info_url = 'https://api.github.com/user'
        user_info_response = requests.get(
            user_info_url, headers={'Authorization': f'token {access_token}'}
        )
        user_info = user_info_response.json()

        user,created = User.objects.get_or_create(username=user_info['login'], email=user_info['email'])
        if created:
            user.set_unusable_password()
            user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid code'}, status=400)


