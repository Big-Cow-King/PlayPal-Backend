import base64
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import serializers

from accounts.serializers import UserSerializer, SportSerializer
from events.models import Event, Sport
from notifications.models import Notification


class EventSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    sport_data = serializers.CharField(write_only=True)
    attachment_data = serializers.CharField(write_only=True, required=False,
                                            allow_blank=True, allow_null=True)
    owner = UserSerializer(read_only=True)
    admins = UserSerializer(read_only=True, many=True)
    players = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = (
            'id', 'owner', 'start_time', 'end_time', 'title',
            'attachment', 'description', 'content', 'sport', 'sport_data',
            'players', 'level', 'age_group', 'visibility', 'max_players', 'admins',
            'location', 'attachment_data', 'created_at', 'updated_at'
        )
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'owner', 'players', 'admins'
        ]

    def create(self, validated_data):
        sport_data = validated_data.pop('sport_data').lower()
        attachment_data = validated_data.pop('attachment_data', None)
        if attachment_data:
            format, imgstr = attachment_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name=f'event-{validated_data["title"]}.{ext}')
            validated_data['attachment'] = data
        players = validated_data.pop('players', [])
        admins = validated_data.pop('admins', [])
        admins.append(self.context['request'].user)
        event = Event.objects.create(owner=self.context['request'].user,
                                     **validated_data)
        event.sport = Sport.objects.get_or_create(name=sport_data)[0]
        event.players.set(players)
        event.admins.set(admins)
        event.save()

        return event

    def update(self, instance, validated_data):
        validated_data_copy = validated_data.copy()
        instance.updated_at = timezone.now()
        instance.start_time = validated_data.pop('start_time',
                                                 instance.start_time)
        instance.end_time = validated_data.pop('end_time', instance.end_time)
        instance.title = validated_data.pop('title', instance.title)
        instance.visibility = validated_data.pop('visibility',
                                                 instance.visibility)
        instance.description = validated_data.pop('description',
                                                  instance.description)
        instance.content = validated_data.pop('content', instance.content)
        instance.max_players = validated_data.pop('max_players',
                                                  instance.max_players)
        sport_data = validated_data.pop('sport_data', '').lower()
        instance.sport = Sport.objects.get_or_create(name=sport_data)[0]

        try:
            attachment_data = validated_data.pop('attachment_data')
            if attachment_data:
                format, imgstr = attachment_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr),
                                   name=f'event-{instance.title}.{ext}')
                instance.attachment = data
            else:
                instance.attachment = None
        except KeyError:
            pass

        instance.players.set(
            validated_data.get('players', instance.players.all()))
        instance.admins.set(
            validated_data.get('admins', instance.admins.all()))
        instance.save()
        notification(instance, validated_data_copy)
        return instance


def notification(instance, validated_data):
    # Convert keys to strings and join them with commas
    content = ', '.join([f'{key}: {value}' for key, value in validated_data.items()])
    description = f'The following detail has been changed - {content}'
    for user in instance.players.all():
        Notification.objects.create(player_id=user, event_id=instance,
                                    description=description)
