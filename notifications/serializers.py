from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event_id.title', read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'event_id', 'event_title', 'description', 'created_at', 'read')
        read_only_fields = ['id', 'event_id', 'event_title', 'description', 'created_at']

    def update(self, instance, validated_data):
        instance.read = True
        instance.save()
        return instance
