from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='first_name', required=False)

    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name')
        )
        return user

    def update(self, instance: User, validated_data) -> User:
        instance: User = super().update(instance, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = 'id', 'username', 'password', 'fullname', 'email', 'avatar', 'phone', 'qrcode', 'is_staff'
