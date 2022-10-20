import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.id}/{filename}'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True
    )
    phone = models.CharField(
        max_length=12, null=True, blank=True, verbose_name='Телефон'
    )
    qrcode = models.BinaryField(blank=True, null=True, verbose_name='QRCode')
