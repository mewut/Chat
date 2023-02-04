from django.db import models
from django.contrib.auth.models import User
from chat.models import Room
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(max_length=50, unique=True, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='default.gif', upload_to='media', height_field=270, width_field=150, blank=True, null=True)
    online = models.BooleanField(default=False)

    def user_list(self):
        users = Profile.objects.filter().order_by('name')
        return list(users)

    def room_list(self):
        rooms = Room.objects.filter().ordef_by('name')
        return list(rooms)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)
