from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'location']
        # extra_kwargs = {'password': {'write_only': True}}   # this is only for hide

    #
    def create(self, validated_data):
        """
        Create and return a new User instance,given to validate data
        """
        return User.objects.create_user(**validated_data)
