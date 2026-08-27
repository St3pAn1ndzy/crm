from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    role = models.CharField(
        max_length=50, default="manager", verbose_name="Роль в системе"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
