import binascii
import os
from django.conf import settings
from django.db import models


class TokenGsoft(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        related_name='authtoken',
        on_delete=models.CASCADE, 
        verbose_name="User"
    )       
    created = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"


class DeviceTokenGsoft(models.Model):
    ip = models.CharField(
        max_length=50,
    )
    browser = models.CharField(
        max_length=255,
    )
    token = models.OneToOneField(
        TokenGsoft,
        on_delete=models.CASCADE,
        related_name='device_token',
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Device token Gsoft'
        verbose_name_plural = 'Devices Token Gsoft'
        db_table = 'device_token_Gsoft'
