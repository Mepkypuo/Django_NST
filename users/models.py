from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    training_organization = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
