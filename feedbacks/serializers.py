from django.utils import timezone
from rest_framework import serializers

from feedbacks.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Feedback
        fields = (
            'id', 'content', 'rate', 'user_id', 'event', 'event_id', 'created_at',
            'updated_at')
        read_only_fields = (
            'id', 'user_id', 'event', 'created_at', 'updated_at')

    def create(self, validated_data):
        return Feedback.objects.create(user_id=self.context['request'].user,
                                       **validated_data)

    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        instance.content = validated_data.get('content', instance.content)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance
