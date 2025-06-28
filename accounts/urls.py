from django.urls import path
from .views import SignupAPIView, LoginView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


app_name = 'accounts'

urlpatterns = [
    path('register/', SignupAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='Login'),
    # path('logout/', LogoutView.as_view(), name='Logout'),

    path('profile/', ProfileView.as_view(), name='user-profile'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]