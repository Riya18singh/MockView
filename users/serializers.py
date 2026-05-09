from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'phone', 'experience_level',
            'target_role', 'target_companies', 'resume',
            'resume_text', 'skills', 'profile_completed',
            'created_at'
        ]
        read_only_fields = [
            'id', 'username', 'email',
            'resume_text', 'created_at'
        ]


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone',
            'experience_level', 'target_role',
            'target_companies', 'resume'
        ]

    def update(self, instance, validated_data):
        # If new resume uploaded, clear old parsed text
        if 'resume' in validated_data:
            instance.resume_text = None
            instance.skills = []
        return super().update(instance, validated_data)