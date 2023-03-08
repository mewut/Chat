from rest_framework import serializers
from django.contrib.auth.models import User
from chat.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class RoomSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    invited = UserSerializer(many=True)
    class Meta:
        model = Room
        fields = ('id', 'owner', 'members')


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Message
        fields = ('user', 'text')


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('room', 'text')
        