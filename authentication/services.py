from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from users.models import CustomUser
from common.exceptions import APIException
from django.conf import settings

class AuthService:
    MAX_FAILED_ATTEMPTS = 5
    LOCK_TIME = timedelta(minutes=15)

    @staticmethod
    def authenticate_user(email, password, action="login"):
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise APIException("INVALID_CREDENTIALS", "Invalid email or password.", status_code=401)

        # Account locked
        if user.lock_until and now() < user.lock_until:
            raise APIException(
                "ACCOUNT_LOCKED",
                f"Too many failed attempts. Try again after {user.lock_until}.",
                status_code=403
            )

        # Wrong password
        if not check_password(password, user.password):
            user.failed_attempts += 1
            if user.failed_attempts >= AuthService.MAX_FAILED_ATTEMPTS:
                user.lock_until = now() + AuthService.LOCK_TIME
            user.save()
            raise APIException("INVALID_CREDENTIALS", "Invalid email or password.", status_code=401)

        # Successful login
        user.failed_attempts = 0
        user.lock_until = None
        user.save()

        tokens = AuthService.generate_jwt_token(user)
        response_data = {"accessToken": tokens["accessToken"], "expiresIn": tokens["expiresIn"], "message": "Login successful"}

        if action != "login":
            response_data.update({
                "message": "User registered successfully",
                "user": {"id": user.id, "email": user.email},
            })
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        response = Response(response_data, status=status_code)
        AuthService.set_refresh_token_cookie(response, tokens["refreshToken"])
        return response

    @staticmethod
    def generate_jwt_token(user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        return {
            "refreshToken": str(refresh),
            "accessToken": str(access_token),
            "expiresIn": int(access_token['exp'] - access_token['iat'])
        }

    @staticmethod
    def set_refresh_token_cookie(response, refresh_token):
        is_secure = not settings.DEBUG
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=is_secure,
            samesite="None",
            max_age=7 * 24 * 60 * 60,
        )

    @staticmethod
    def update_user_password(user, new_password, blacklist_tokens=True):
        user.set_password(new_password)
        user.last_password_reset = now()
        user.save()
        if blacklist_tokens:
            AuthService.blacklist_all_tokens(user)

    @staticmethod
    def blacklist_all_tokens(user):
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
