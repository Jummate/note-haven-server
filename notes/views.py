
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST','GET'])
def notes_view(request):
    if request.method == 'POST':
        print(request.data)
        return Response({"message":"Note created succesfully"}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        return Response({"message":"notes"}, status=status.HTTP_200_OK)

@api_view(['GET','PUT','PATCH','DELETE'])
def note_detail(request):
    if request.method == 'GET':
        return Response({"message":"Note created succesfully"}, status=status.HTTP_201_CREATED)
