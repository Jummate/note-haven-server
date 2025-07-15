
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from notes.models import Note
from notes.serialisers import NoteSerializer


@api_view(['POST','GET'])
def notes_view(request):
    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            note = serializer.save()
            response_data = NoteSerializer(note).data
            return Response({"message":"Note created succesfully", "data":response_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        user = request.user
        notes = Note.objects.filter(user=user).order_by('-updated_at')
        response_data = NoteSerializer(notes, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET','PUT','PATCH','DELETE'])
def note_detail(request):
    if request.method == 'GET':
        return Response({"message":"Note created succesfully"}, status=status.HTTP_201_CREATED)
