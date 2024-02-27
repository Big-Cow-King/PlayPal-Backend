from django.db import models

from accounts.models import User
from events.models import Event


# Create your models here.
class Notification(models.Model):
    player_id = models.ForeignKey(User, related_name='notifications',
                                  on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.player_id.username} - {self.event_id.title} - {self.description}'
