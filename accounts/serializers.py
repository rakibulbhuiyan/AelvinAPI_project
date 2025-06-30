from django.utils import timezone
from .models import User,Profile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta 


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'email', 'display_name', 'bio', 'profile_picture', 'banner', 'location',
            'website', 'language', 'gender', 'google_connected', 'apple_connected'
        ]

class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name','last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class OTPVerifyLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email")

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        if user.otp_exp < timezone.now():
            raise serializers.ValidationError("OTP expired")

        user.otp_verified = True
        user.save()
        data['user'] = user
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data['user'] = user
        return data

# class AccountDeleteSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#     reason = serializers.CharField(required=False, allow_blank=True)

#     def validate(self, data):
#         user = authenticate(username=data['username'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError("Invalid username or password")
#         data['user'] = user
#         return data
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email= serializers.EmailField()
    
    def validate_email(self,data):
        try:
            user= User.objects.get(email=data)
        except:
            raise serializers.ValidationError("This Email does not exist!")
        
         
        user.generate_otp()
        send_mail(
             "Password Reset OTP",
            f"Your OTP for password reset is {user.otp}",
            "rocky@gmail.com",
            [user.email],
            fail_silently=False,
        )
        return data
    
class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User not found."})

        # Check if OTP is correct and not expired
        if user.otp != data["otp"]:
            raise serializers.ValidationError({"otp": "Invalid OTP."})

        if user.otp_exp < now():  # OTP expired
            raise serializers.ValidationError({"otp": "OTP expired."})

        # Mark OTP as verified
        user.otp_verified = True
        user.save()

        return data

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user=User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User not found."})
        
        # check if OTP was verified
        if not user.otp_verified:
            raise serializers.ValidationError({"otp": "OTP verification required."})

        return data
    
    def save(self,**kwargs):
        user=User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.otp = None # clear otp after reset
        user.otp_exp = None
        user.otp_verified = False
        user.save()
        return user
    
        