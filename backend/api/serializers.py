from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
    
    class Meta:
        model = User
        fields = '__all__'
