from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            alias=validated_data.get('alias')
        )
        return user
    
    class Meta:
        model = User
        fields = 'id', 'username', 'password', 'first_name', 'email', 'avatar', 'phone', 'alias', 'qrcode', 'is_staff'
