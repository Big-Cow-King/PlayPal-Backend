from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=40, blank=True, null=True)
    sports_you_can_play = models.ManyToManyField(Sport, blank=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    email_product = models.BooleanField(default=False)
    email_security = models.BooleanField(default=False)
    phone_security = models.BooleanField(default=False)

    def __str__(self):
        return self.username
