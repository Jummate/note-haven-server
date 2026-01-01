from rest_framework import serializers
from common.exceptions import APIException  # your standardized error
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

    def validate_title(self, value):
        if not value:
            raise APIException("VALIDATION_ERROR", "Title is required.")
        if len(value) > 255:
            raise APIException("VALIDATION_ERROR", "Title must be 255 characters or less.")
        return value

    def validate_content(self, value):
        if not value:
            raise APIException("VALIDATION_ERROR", "Content is required.")
        return value

    def validate_input_tags(self, value):
        if value and not isinstance(value, list):
            raise APIException("VALIDATION_ERROR", "Tags must be provided as a list.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        tags_data = validated_data.pop('input_tags', [])

        try:
            note = Note.objects.create(user=user, **validated_data)
        except Exception as e:
            raise APIException("SERVER_ERROR", f"Could not create note: {str(e)}")

        try:
            tag_objs = get_or_create_user_tags(tags_data, user)
            note.tags.set(tag_objs)
        except Exception as e:
            raise APIException("SERVER_ERROR", f"Could not attach tags: {str(e)}")

        return note

