from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=50, unique=True)
    owner = models.ForeignKey(User, related_name='owner', default=User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members', blank=False, default=owner)

    def __str__(self):
        return f'{self.room_name}_{self.pk}'

    class Meta:
        ordering = ('owner', 'pk')


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    text = models.CharField(max_length=2555)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
