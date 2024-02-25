from django.db import models


# Create your models here.

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Event(models.Model):
    level_choices = {
        'B': 'Beginner',
        'I': 'Intermediate',
        'A': 'Advanced',
        'P': 'Professional'
    }

    age_group_choices = {
        'C': 'Children',
        'T': 'Teenagers',
        'A': 'Adults',
        'S': 'Seniors'
    }

    visibility_choices = {
        'Public': 'Public',
        'Private': 'Private'
    }

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=100)
    attachment = models.ImageField(upload_to='events/attachments/',
                                   null=True, blank=True)
    description = models.TextField(max_length=1000)
    content = models.TextField()
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE,
                              related_name='events', null=True, blank=True)
    players = models.ManyToManyField('auth.User', blank=True)  # TODO: Need to be edit after merging with user app
    level = models.TextField(choices=level_choices.items())
    age_group = models.TextField(choices=age_group_choices.items())
    visibility = models.TextField(choices=visibility_choices.items(), default='Public')
    max_players = models.IntegerField()
    owner = models.ForeignKey('auth.User', related_name='events',
                              on_delete=models.CASCADE, null=True, blank=True,
                              default=None)  # TODO: Need to be edited after merging with user app
    admins = models.ManyToManyField('auth.User', related_name='admin_events', blank=True)  # TODO: Need to be edited after merging with user app
    location = models.CharField(max_length=100)
