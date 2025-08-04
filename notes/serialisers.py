# from rest_framework import serializers
# from tags.serialisers import TagInputSerializer

# from .models import Note
# from .utils import get_or_create_user_tags

# class NoteSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     content = serializers.CharField()
#     is_archived = serializers.BooleanField(default=False)
#     tags = TagInputSerializer(many=True, required=False)

#     def create(self, validated_data):
#         user = self.context['request'].user
#         tags_data = validated_data.pop('tags', [])

#         note = Note.objects.create(user=user, **validated_data)
#         tag_objs = get_or_create_user_tags(tags_data, user)
#         note.tags.set(tag_objs)
#         return note

# notes/serializers.py

from rest_framework import serializers
from tags.serialisers import TagSerializer, TagInputSerializer
from .models import Note
from .utils import get_or_create_user_tags

class NoteSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    input_tags = TagInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Note
        fields = [
            'id',
            'user_id',
            'title',
            'content',
            'is_archived',
            'created_at',
            'updated_at',
            'tags',
            'input_tags',
        ]
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at', 'tags']

    def create(self, validated_data):
        user = self.context['request'].user
        tags_data = validated_data.pop('input_tags', [])
        note = Note.objects.create(user=user, **validated_data)
        tag_objs = get_or_create_user_tags(tags_data, user)
        note.tags.set(tag_objs)
        return note
