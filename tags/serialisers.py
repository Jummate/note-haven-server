from rest_framework import serializers

class TagInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)