from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from users.serialisers import SignupSerializer
# Create your views here.
@api_view(['POST'])
def create_new_user(request):
    if request.method == 'POST':
        print("resuest", request.data)
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
             user = serializer.save()
             return Response({"message": "User registered successfully", "user": {
                        "id": user.id,
                        "email": user.email,
                    },}, status=status.HTTP_201_CREATED)
        print("error", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
