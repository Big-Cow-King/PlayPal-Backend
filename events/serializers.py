from django.utils import timezone
from rest_framework import serializers

from events.models import Attachment, Event, Sport


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        return Attachment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.file = validated_data.get('file')
        instance.save()
        return instance


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
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner', 'admins', 'players']
        sports = SportSerializer(many=True)

    def create(self, validated_data):
        created_at = timezone.now()
        updated_at = timezone.now()
        attachments = validated_data.pop('attachments')
        sports = validated_data.pop('sports')
        event = Event.objects.create(created_at=created_at,
                                     updated_at=updated_at,
                                     owner=self.context['request'].user,
                                     **validated_data)
        for attachment in attachments:
            Attachment.objects.create(event=event, **attachment)
        for name in sports:
            name = name.lower()
            try:
                sport = Sport.objects.get(name=name)
            except Sport.DoesNotExist:
                sport = Sport.objects.create(name=name)
            event.sports.add(sport)
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
        sports = validated_data.pop('sports')
        if sports:
            for name in sports:
                name = name.lower()
                try:
                    sport = Sport.objects.get(name=name)
                except Sport.DoesNotExist:
                    sport = Sport.objects.create(name=name)
                instance.sports.set(sport)

        attachments = validated_data.pop('attachments', [])
        if attachments:
            for attachment in attachments:
                Attachment.objects.create(event=instance, **attachment)

        instance.players.set(
            validated_data.get('players', instance.players.all()))
        instance.admins.set(
            validated_data.get('admins', instance.admins.all()))
        instance.save()
        return instance
