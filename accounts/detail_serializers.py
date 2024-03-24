from rest_framework import serializers

from accounts.models import User
from accounts.serializers import SportSerializer
from events.serializers import EventSerializer


class UserDetailSerializer(serializers.ModelSerializer):
    sports_you_can_play = SportSerializer(read_only=True, many=True)
    join_events = EventSerializer(read_only=True, many=True)
    own_events = EventSerializer(read_only=True, many=True)
    admin_events = EventSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'name', 'gender',
            'sports_you_can_play', 'phone_no', 'age', 'description',
            'avatar', 'email_product', 'email_security', 'phone_security',
            'join_events', 'own_events', 'admin_events'
        )
