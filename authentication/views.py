from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serialisers import SignupSerializer, LoginSerializer
from .services import AuthService


# Create your views here.
@api_view(['POST'])
def create_new_user(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
             user = serializer.save()
             return Response({"message": "User registered successfully", "user": {
                        "id": user.id,
                        "email": user.email,
                    },}, status=status.HTTP_201_CREATED)
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
            


    
       
