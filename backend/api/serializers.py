from rest_framework import serializers

from .models import QRCode, User


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='first_name', required=True)

    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
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
        fields = (
            'id',
            'username',
            'password',
            'fullname',
            'email',
            'avatar',
            'phone',
            'qrcode',
        )


class QRCodeGenerationSerializer(serializers.ModelSerializer):
    data = serializers.CharField(source='id', required=False)

    def create(self, _):
        return QRCode.objects.create()

    class Meta:
        model = QRCode
        fields = (
            'data',
            'dt_created',
        )
        validators = []
