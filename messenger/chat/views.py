from django.shortcuts import render
from django.http import JsonResponse
from .models import Profile, Room
from .serializers import RoomSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet


def api_users(request):
    if request.method == 'GET':
        users = Profile.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class ApiUsers(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer


class ApiRooms(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
