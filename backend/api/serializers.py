import datetime as dt
from math import ceil

import pytz
from rest_framework import serializers

from .config import TARIFF_PER_MINUTE, TARIFF_START
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
            'is_staff',
        )
        read_only_fields = (
            'id',
            'is_staff',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }


class QRCodeGenerationSerializer(serializers.ModelSerializer):
    data = serializers.UUIDField(source='id', required=False)

    def create(self, kwargs: dict):
        return QRCode.objects.create(user=kwargs.get('user'))

    class Meta:
        model = QRCode
        fields = (
            'data',
            'dt_created',
        )
        validators = []
        read_only_fields = (
            'data',
            'dt_created',
        )


class QRCodeScanSerializer(QRCodeGenerationSerializer):
    def update(self, instance: QRCode, _):
        instance.closed = True
        instance.dt_payment = dt.datetime.now(tz=pytz.UTC)
        instance.cost = TARIFF_START
        placement_duration = instance.dt_payment - instance.dt_created
        total_seconds = ceil(placement_duration.total_seconds())
        total_minutes = total_seconds // 60 + (total_seconds % 60 != 0)
        instance.cost += TARIFF_PER_MINUTE * total_minutes
        instance.save()
        return instance

    class Meta(QRCodeGenerationSerializer.Meta):
        fields = (
            'data',
            'dt_created',
            'dt_payment',
            'cost',
        )
        read_only_fields = (
            'data',
            'dt_created',
            'dt_payment',
            'cost',
        )
