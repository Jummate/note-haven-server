
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from notes.serialisers import TagSerializer

@api_view(['GET'])
def tags_view(request):
    try:
        tags = request.user.tags.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': 'Something went wrong while fetching tags.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

