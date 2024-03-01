import base64
from django.core.files.base import ContentFile
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User, Sport


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        return Sport.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    sports_you_can_play = SportSerializer(read_only=True, many=True)
    sports_data = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,
                                     validators=[validate_password])
    avatar_data = serializers.CharField(write_only=True, required=False,
                                        allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'name', 'gender', 'sports_data',
                  'sports_you_can_play', 'phone_no', 'age', 'description',
                  'avatar', 'email_product', 'email_security', 'phone_security',
                  'avatar_data')

        read_only_fields = ['id', 'avatar', 'email_product', 'email_security',
                            'phone_security']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=True  # Add this line to set is_active field
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))

        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.age = validated_data.get('age', instance.age)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.email_product = validated_data.get('email_product',
                                                    instance.email_product)
        instance.email_security = validated_data.get('email_security',
                                                     instance.email_security)
        instance.phone_security = validated_data.get('phone_security',
                                                     instance.phone_security)
        try:
            avatar_data = validated_data.pop('avatar_data')
            if avatar_data:
                format, imgstr = avatar_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr),
                                   name=f'{instance.username}.{ext}')
                instance.avatar = data
            else:
                instance.avatar = None
        except KeyError:
            pass

        sports_names = validated_data.get('sports_data', None)
        if sports_names is not None:
            sports_names = sports_names.replace('\\"', '').replace('"', '').strip('][').split(', ')
            sports_instances = []
            for name in sports_names:
                sport, created = Sport.objects.get_or_create(name=name)
                sports_instances.append(sport)

            instance.sports_you_can_play.set(sports_instances)
        else:
            instance.sports_you_can_play.clear()

        instance.save()
        return instance
