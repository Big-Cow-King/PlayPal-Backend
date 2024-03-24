from rest_framework import serializers

from accounts.serializers import UserSerializer
from events.serializers import EventSerializer
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    event_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'user', 'event', 'amount', 'date', 'user_id', 'event_id')
        read_only_fields = ['date', 'user', 'event']
