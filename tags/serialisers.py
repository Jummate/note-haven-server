from rest_framework import serializers
from .models import Tag

class TagInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)

class TagSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id')

    class Meta:
        model = Tag
        fields = ['id', 'name', 'user_id']