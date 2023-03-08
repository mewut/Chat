from django.http import JsonResponse
from .models import UserProfile, Room
from app.serializers import *
from rest_framework.viewsets import ModelViewSet


def api_users(request):
    # if request.user.is_authenticated:
    #     if not UserProfile.objects.filter(user=request.user).exists():
    #         add_user = UserProfile()
    #         add_user.user = request.user
    #         add_user.save()
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)



class ApiUsers(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class ApiRooms(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    