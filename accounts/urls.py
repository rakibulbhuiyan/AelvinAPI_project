from django.urls import path
from .views import (SignupAPIView, ProfileView, AccountDeleteView, PasswordResetRequestAPIView, OTPVerificarionAPIView, PasswordResetAPIView,
                    LoginSendOTPView, OTPVerifyingLoginView)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView



app_name = 'accounts'

urlpatterns = [
    path('register/', SignupAPIView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='Login'),
    # path('logout/', LogoutView.as_view(), name='Logout'),
    path('login/', LoginSendOTPView.as_view(), name='login-send-otp'),
    path('verify-otp/', OTPVerifyingLoginView.as_view(), name='otp-verify-login'),

    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('delete/', AccountDeleteView.as_view(), name='delete-account'),

    path("password-reset/request/", PasswordResetRequestAPIView.as_view(), name="password-reset-request"),
    path("password-reset/verify-otp/", OTPVerificarionAPIView.as_view(), name="password-reset-verify-otp"),  # New API
    path("password-reset/change-password/", PasswordResetAPIView.as_view(), name="password-reset-change"),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    
]