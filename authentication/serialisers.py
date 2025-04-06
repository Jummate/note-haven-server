from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta
from django.utils.timezone import now



from users.models import CustomUser

class SignupSerializer(serializers.Serializer):
    # id = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        #  # Optional: Add password strength validation
        # if not any(char.isdigit() for char in password):
        #     raise serializers.ValidationError("Password must contain at least one digit.")
        # if not any(char.isalpha() for char in password):
        #     raise serializers.ValidationError("Password must contain at least one letter.")
    
    
        return attrs
    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def create(self, validated_data):
    # Hash the password and create the user
        return CustomUser.objects.create(
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if not email or not password:
            raise serializers.ValidationError({"detail":"Email and password are required"}, code=400)
        # try:
        #     user = CustomUser.objects.get(email=email)
        # except CustomUser.DoesNotExist:
        #     raise serializers.ValidationError({"detail": "Invalid credentials"}, code=404)
        
        return attrs
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        if not password:
            raise serializers.ValidationError({"detail":"Password is required"}, code=400)
        # try:
        #     user = CustomUser.objects.get(email=email)
        # except CustomUser.DoesNotExist:
        #     raise serializers.ValidationError({"detail": "Invalid credentials"}, code=404)
        
        return attrs
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
class ForgotPasswordSerializer(serializers.Serializer):
         email = serializers.EmailField()
         def validate_email(self, value):
            if "@" not in value:
                raise serializers.ValidationError("Invalid email format.")
            return value