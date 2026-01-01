from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from notes.models import Note
from notes.serialisers import NoteSerializer

from common.exceptions import APIException

@api_view(['POST','GET'])
def notes_view(request):
    if request.method == 'POST':
        serializer = NoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            note = serializer.save()
            response_data = NoteSerializer(note).data
            return Response({"message":"Note created successfully", "data":response_data}, status=status.HTTP_201_CREATED)
        # Normalize serializer errors
        raise APIException("VALIDATION_ERROR", serializer.errors)
    
    elif request.method == 'GET':
        user = request.user
        notes = Note.objects.filter(user=user).order_by('-updated_at')
        response_data = NoteSerializer(notes, many=True).data
        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET','PUT','PATCH','DELETE'])
def note_detail(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        raise APIException("NOT_FOUND", "Note not found")
    
    if request.method == 'DELETE':
        note.delete()
        return Response({"message":"Note deleted successfully"}, status=status.HTTP_200_OK)
    

@api_view(['PATCH'])
def archive_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        raise APIException("NOT_FOUND", "Note not found")
    note.is_archived = True
    note.save()
    return Response({"message":"Note archived successfully"}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def restore_note(request, note_id):
    try:
        note = Note.objects.get(id=note_id, user=request.user)
    except Note.DoesNotExist:
        raise APIException("NOT_FOUND", "Note not found")
    note.is_archived = False
    note.save()
    return Response({"message":"Note restored successfully"}, status=status.HTTP_200_OK)
