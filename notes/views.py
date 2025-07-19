
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
def note_detail(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except note.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        note.delete()
        return Response({"message":"Note deleted succesfully"}, status=status.HTTP_200_OK)
    
@api_view(['PATCH'])
def archive_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except note.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    note.is_archived = True
    note.save()
    return Response({"message":"Note archived succesfully"}, status=status.HTTP_200_OK)
        
