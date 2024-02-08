import base64
from django.utils import timezone
from rest_framework import serializers

from events.models import Event, Sport


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        return Sport.objects.create(**validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']

        sport = SportSerializer(read_only=True)
        sport_data = serializers.CharField(write_only=True)
        attachment_data = serializers.CharField(write_only=True)

    def create(self, validated_data):
        sport_data = validated_data.pop('sport_data').lower()
        attachment_data = validated_data.pop('attachment_data')
        if attachment_data:
            validated_data['attachment_data'] = base64.b64decode(attachment_data)
        event = Event.objects.create(owner=self.context['request'].user,
                                     **validated_data)
        event.sport = Sport.objects.get_or_create(name=sport_data)[0]

        return event

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        instance.start_time = validated_data.pop('start_time', instance.start_time)
        instance.end_time = validated_data.pop('end_time', instance.end_time)
        instance.title = validated_data.pop('title', instance.title)
        instance.description = validated_data.pop('description',
                                                  instance.description)
        instance.content = validated_data.pop('content', instance.content)
        instance.max_players = validated_data.pop('max_players',
                                                  instance.max_players)
        sport_data = validated_data.pop('sport').lower()
        instance.sport = Sport.objects.get_or_create(name=sport_data)[0]

        instance.players.set(
            validated_data.get('players', instance.players.all()))
        instance.admins.set(
            validated_data.get('admins', instance.admins.all()))
        instance.save()
        return instance
