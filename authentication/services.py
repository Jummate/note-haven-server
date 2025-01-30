
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from users.models import CustomUser

class AuthService():

    MAX_FAILED_ATTEMPTS = 5
    LOCK_TIME = timedelta(minutes=15)

    @staticmethod
    def authenticate_user(email, password):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password.")

        # Check if the account is locked
        if user.lock_until and now() < user.lock_until:
            raise AuthenticationFailed(f"Account is temporarily locked. Try again after {user.lock_until}.")
        
        if not check_password(password, user.password):
            # Increment failed attempts
            user.failed_attempts += 1
            if user.failed_attempts >= AuthService.MAX_FAILED_ATTEMPTS:
                user.lock_until = now() + AuthService.LOCK_TIME
            user.save()
            raise AuthenticationFailed("Invalid email or password.")
        
        # Reset failed attempts on successful login

        tokens = AuthService.generate_jwt_token(user)
        response = Response(
            {"access": tokens["access"], "message": "Login successful"}, status=status.HTTP_200_OK
        )
        AuthService.set_refresh_token_cookie(response, tokens["refresh"])
        user.failed_attempts = 0
        user.lock_until = None
        user.save()

        return response
    
    @staticmethod
    def generate_jwt_token(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    
    def set_refresh_token_cookie(response, refresh_token):
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,  # Prevent JavaScript access
            secure=True,  # Ensure cookies are sent over HTTPS
            samesite="Lax",  # Restrict cross-site requests
            max_age=7 * 24 * 60 * 60,  # Set expiration for 7 days
        )


