# from django.shortcuts import render
# from django.contrib.auth.hashers import make_password, check_password
# from datetime import timedelta, datetime, timezone

from django.utils import timezone
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from users.models import CustomUser
from .serialisers import SignupSerializer, LoginSerializer, ResetPasswordSerializer, ForgotPasswordSerializer
from .services import AuthService
from common.utils.generate_token import generate_reset_token, verify_reset_token
from common.utils.generate_password_reset_link import generate_password_reset_link
from common.utils.generate_email_template import generate_html_template
from common.services.email_service import forward_mail



# Create your views here.
@api_view(['POST'])
def create_new_user(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = serializer.save()
            # return Response({"message":"Account created succesfully"}, status=status.HTTP_201_CREATED)
            response = AuthService.authenticate_user(email, password, action="signup")
            return response 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                response = AuthService.authenticate_user(email, password)
                return response
            except AuthenticationFailed as e:
                return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({"detail": "No refresh token provided"}, status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({"message": "Logout successful"}, status.HTTP_200_OK)
            response.delete_cookie("refresh_token")
            return response
        except:
            return Response({"detail": "Invalid token"}, status.HTTP_400_BAD_REQUEST)
        
@api_view(["POST"])
def reset_password(request):
     serializer = ResetPasswordSerializer(data=request.data)
     if serializer.is_valid():
        token = request.data.get("token")

        new_password = serializer.validated_data["password"]
        email = verify_reset_token(token)

        if not email:
            return Response({"detail": "Invalid or missing reset token"}, status.HTTP_400_BAD_REQUEST)
         
        user = CustomUser.objects.get(email=email)
        user.set_password(new_password)
        user.last_password_reset = timezone.now()
        user.save()
        return Response({"message": "Password reset successful"}, status.HTTP_200_OK)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def forgot_password(request):
     if request.method == "POST":
         serializer = ForgotPasswordSerializer(data=request.data)
         if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            reset_token = generate_reset_token(user)
            reset_link = generate_password_reset_link(reset_token)
            html_template = generate_html_template("Omololu Jumat", "Yakub Jumat", reset_link)
            # add email into recipient_list later
            forward_mail(subject="Reset Your Password", from_email=settings.EMAIL_HOST_USER, recipient_list=["yakubjumat@gmail.com"], html_message=html_template)
            return Response({"message": "Email sent successfully", "email":email}, status.HTTP_200_OK)

     


    
       
