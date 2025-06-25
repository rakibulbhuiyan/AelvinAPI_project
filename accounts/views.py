from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.conf import settings

from .serializers import LoginSerializer,SignupSerializer

class SignupAPIView(APIView):
     def post(self, request):
          serializer = SignupSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          data = serializer.data
          response = status.HTTP_201_CREATED
    
          return Response(data, status=response)
     
class LoginView(APIView):
    
     def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user'] 

        refresh = RefreshToken.for_user(user)

        return Response({
            'success': True,
            'message': 'Login successful',
            'status_code': '200',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_200_OK)