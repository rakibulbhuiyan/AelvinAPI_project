from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from aelvin import settings
from .serializers import (LoginSerializer, SignupSerializer, ProfileSerializer, OTPVerifyLoginSerializer,
                          PasswordResetRequestSerializer, OTPVerificationSerializer, PasswordResetSerializer)
from .models import User, Profile, AccountDeleteLog
from django.core.mail import send_mail

class AccountDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reason = request.data.get('reason', '')

        # Save delete reason in log
        AccountDeleteLog.objects.create(
            user=request.user,
            reason=reason
        )

        # Delete the user
        request.user.delete()

        return Response({
            "success": True,
            "message": "Account deleted successfully"
        }, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Save the user
        # Re-serialize to return accurate data (without password)
        response_data = SignupSerializer(user).data
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginSendOTPView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']

        if not user.is_active:
            user.generate_otp()

            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is {user.otp}. It will expire in 10 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({
                "success": True,
                "message": "OTP sent to your email. Please verify to login."
            }, status=status.HTTP_200_OK)
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'status_code': '200',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            # 'user': serializer.data
        }, status=status.HTTP_200_OK)
        
    
class OTPVerifyingLoginView(APIView):
    def post(self,request):
        serializer = OTPVerifyLoginSerializer(data= request.data)
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


# class LoginView(APIView):
    
#      def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user'] 

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             'success': True,
#             'message': 'Login successful',
#             'status_code': '200',
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user': serializer.data
#         }, status=status.HTTP_200_OK)
     
class PasswordResetRequestAPIView(APIView):
    permission_classes=[]
    def post(self,request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"success": True, "message": "OTP sent to email."}, 
                status=status.HTTP_200_OK
            )
        return Response(
            {"success": False, "errors": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class OTPVerificarionAPIView(APIView):
    permission_classes = []
    def post(self,request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
             return Response(
                {"success": True, "message": "OTP verified successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
class PasswordResetAPIView(APIView):
    permission_class = []

    def post(self,request):
        serializer = PasswordResetSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Password reset successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


























