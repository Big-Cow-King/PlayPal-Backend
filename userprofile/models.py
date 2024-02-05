from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    sports_you_can_play = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    email_product = models.BooleanField(default=False)
    email_security = models.BooleanField(default=False)
    phone_security = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"
