from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='')  # TODO: дописать и проверить
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='Телефон')
    alias = models.CharField(max_length=111, null=True, blank=True, verbose_name='Ник')
    qrcode = models.BinaryField(blank=True, null=True, verbose_name='QRCode')

# Create your models here.
