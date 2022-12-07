import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.id}/{filename}'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='Телефон')


class QRCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    closed = models.BooleanField(default=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_payment = models.DateTimeField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, related_name='qrcodes', on_delete=models.CASCADE, blank=True, null=True)
