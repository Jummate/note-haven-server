
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.models import CustomUser
from .serialisers import (
    SignupSerializer, LoginSerializer, ChangePasswordSerializer,
    ResetPasswordSerializer, ForgotPasswordSerializer
)
from .services import AuthService
from common.exceptions import APIException
from common.utils.generate_token import generate_reset_token, verify_reset_token
from common.utils.generate_password_reset_link import generate_password_reset_link
from common.utils.generate_email_template import generate_html_template
from common.services.email_service import forward_mail
from django.conf import settings

# -------------------
# Signup / Login
# -------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_user(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    user = serializer.save()
    return AuthService.authenticate_user(email, password, action="signup")


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]
    return AuthService.authenticate_user(email, password)

# -------------------
# Logout
# -------------------
@api_view(['POST'])
def logout(request):
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        raise APIException("NO_REFRESH_TOKEN", "No refresh token provided.", status_code=400)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except TokenError:
        raise APIException("INVALID_TOKEN", "Invalid refresh token.", status_code=400)

    response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    response.delete_cookie("refresh_token")
    return response

# -------------------
# Password Reset
# -------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = request.data.get("token")
    email = verify_reset_token(token)
    if not email:
        raise APIException("INVALID_RESET_TOKEN", "Invalid or missing reset token.", status_code=400)

    user = CustomUser.objects.get(email=email)
    AuthService.update_user_password(user, serializer.validated_data["password"])
    return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"]
    try:
        user = CustomUser.objects.get(email=email)
        reset_token = generate_reset_token(user)
        reset_link = generate_password_reset_link(reset_token)
        html_template = generate_html_template("", "Notes Haven", reset_link)
        forward_mail(
            subject="Reset Your Password",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_template
        )
    except CustomUser.DoesNotExist:
        # Silently ignore to avoid email enumeration
        pass

    return Response({"message": "If an account exists, a password reset link has been sent."}, status=status.HTTP_200_OK)

# -------------------
# Change Password
# -------------------
@api_view(["POST"])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)

    new_password = serializer.validated_data["new_password"]
    AuthService.update_user_password(request.user, new_password, blacklist_tokens=True)

    response = Response({"message": "Password successfully changed"}, status=status.HTTP_200_OK)
    response.delete_cookie("refresh_token")
    return response

# -------------------
# Refresh Token
# -------------------
@api_view(["GET"])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        raise APIException("NO_REFRESH_TOKEN", "Could not refresh session. Please log in again.", status_code=401)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
        return Response({
        "accessToken": str(access_token),
        "expiresIn": int(access_token['exp'] - access_token['iat'])
    }, status=status.HTTP_200_OK)


        
        # return Response({"accessToken": str(refresh.access_token)}, status=status.HTTP_200_OK)
    except TokenError:
        raise APIException("INVALID_TOKEN", "Could not refresh session. Please log in again.", status_code=401)
