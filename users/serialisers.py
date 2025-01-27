from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import CustomUser

class SignupSerializer(serializers.Serializer):
    # id = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        #  # Optional: Add password strength validation
        # if not any(char.isdigit() for char in password):
        #     raise serializers.ValidationError("Password must contain at least one digit.")
        # if not any(char.isalpha() for char in password):
        #     raise serializers.ValidationError("Password must contain at least one letter.")
    
    
        return attrs
    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def create(self, validated_data):
    # Hash the password and create the user
        return CustomUser.objects.create(
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )