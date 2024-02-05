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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        sports = SportSerializer(many=True)

    def create(self, validated_data):
        created_at = timezone.now()
        updated_at = timezone.now()
        return Event.objects.create(created_at=created_at,
                                    updated_at=updated_at, **validated_data)

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        instance.start_time = validated_data.pop('start_time',
                                                 instance.start_time)
        instance.end_time = validated_data.pop('end_time', instance.end_time)
        instance.title = validated_data.pop('title', instance.title)
        instance.description = validated_data.pop('description',
                                                  instance.description)
        instance.max_players = validated_data.pop('max_players',
                                                  instance.max_players)
        sports = validated_data.pop('sports', instance.sports)

        if sports:
            for sport in sports:
                try:
                    sport = Sport.objects.get(name=sport)
                except Sport.DoesNotExist:
                    sport = Sport.objects.create(name=sport)
                instance.sports.add(sport)

        instance.players.add(
            *validated_data.get('players', instance.players.all()))
        instance.admins.add(
            *validated_data.get('admins', instance.admins.all()))
        instance.save()
        return instance
