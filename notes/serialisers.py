from rest_framework import serializers
from tags.serialisers import TagInputSerializer

from .models import Note
from .utils import get_or_create_user_tags

class NoteSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    is_archived = serializers.BooleanField(default=False)
    tags = TagInputSerializer(many=True, required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        tags_data = validated_data.pop('tags', [])

        note = Note.objects.create(user=user, **validated_data)
        tag_objs = get_or_create_user_tags(tags_data, user)
        note.tags.set(tag_objs)
        return note

