import base64
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    email = serializers.EmailField(source='user.email')
    avatar_data = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Profile
        fields = ('user', 'name', 'email', 'gender', 'sports_you_can_play',
                  'phone_no', 'age', 'description', 'avatar',
                  'email_product', 'email_security', 'phone_security', 'avatar_data')

    def update(self, instance, validated_data):
        user = instance.user
        user.email = validated_data.get('email', user.email)
        user.password = validated_data.get('password', user.password)
        user.save()
        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.sports_you_can_play = validated_data.get('sports_you_can_play', instance.sports_you_can_play)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.age = validated_data.get('age', instance.age)
        instance.description = validated_data.get('description', instance.description)
        instance.email_product = validated_data.get('email_product', instance.email_product)
        instance.email_security = validated_data.get('email_security', instance.email_security)
        instance.phone_security = validated_data.get('phone_security', instance.phone_security)
        try:
            avatar_data = validated_data.pop('avatar_data')
            if avatar_data:
                format, imgstr = avatar_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{instance.user.username}.{ext}')
                instance.avatar = data
            else:
                instance.avatar = None
        except KeyError:
            pass

        instance.save()
