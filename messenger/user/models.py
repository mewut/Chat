from django.db import models
from django.contrib.auth.models import User
from chat.models import Room
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', max_length=50, unique=True, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.gif', upload_to='media', height_field=270, width_field=150, blank=True, null=True)
    online = models.BooleanField(default=False)

    def chat_list(self):
        chats = set()
        for chat in Room.objects.all():
            if self.user in chat.members.all():
                chats.add(chat)
        return(chats)

    def __str__(self):
        return self.user.username

    def user_list(self):
        users = Profile.objects.filter().order_by('name')
        return list(users)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)
