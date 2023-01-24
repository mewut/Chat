from rest_framework import serializers
from .models import Profile, Room
from django.contrib.auth.models import User


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'name', 'avatar', 'room')
