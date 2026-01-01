
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from common.exceptions import APIException
from notes.serialisers import TagSerializer

@api_view(['GET'])
def tags_view(request):
    try:
        tags = request.user.tags.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except APIException as e:
        return Response({"code": e.code, "message": e.message}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"code": "SERVER_ERROR", "message": "Something went wrong while fetching tags."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
