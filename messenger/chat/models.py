from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField            # https://github.com/SmileyChris/easy-thumbnails


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Profile(models.Model):
    name = models.CharField(max_length=100, unique=True)
   # user_id = models.CharField(max_length=140, default='SOME STRING')
    avatar = ThumbnailerImageField(default='default.gif', resize_source=dict(quality=50, size=(100, 100), sharpen=True))   #сначала я неправильно прописала дефотлную картинку
    room = models.OneToOneField(Room, on_delete=models.SET_NULL, null=True)
    online = models.BooleanField(default=False)

    def user_list(self):
        users = Profile.objects.filter().order_by('name')
        return list(users)


class Message(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
