from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# Get the custom user model
User = get_user_model()

# Serializer for registering a new user
class RegisterSerializer(serializers.ModelSerializer):
    # Email field with uniqueness check
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    # Password field (write-only, required, validated)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    # Second password field for confirmation
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'role', 'phone')

    # Check if both passwords match
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    # Create the user after validation
    def create(self, validated_data):
        validated_data.pop('password2')  # remove confirm password
        user = User.objects.create_user(**validated_data)
        return user


# Serializer for returning logged-in user profile info
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_approved', 'phone')
