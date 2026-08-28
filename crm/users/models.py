from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    ROLE_CHOICES = [
        ("operator", "Оператор"),
        ("marketer", "Маркетолог"),
        ("manager", "Менеджер"),
    ]
    role = models.CharField(max_length=50,
                            choices=ROLE_CHOICES,
                            default="manager",
                            verbose_name="Роль в системе")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.role == "operator":
            group = Group.objects.filter(name="Operators").first()
        elif self.role == "marketer":
            group = Group.objects.filter(name="Marketers").first()
        elif self.role == "manager":
            group = Group.objects.filter(name="Managers").first()
        else:
            group = None

        if group:
            self.groups.clear()
            self.groups.add(group)
