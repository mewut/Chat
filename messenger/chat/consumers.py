import json
from .models import UserProfile, Room, Message
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# https://django.fun/ru/articles/tutorials/django-websockety-i-channels/


def userlist():
    objects = UserProfile.objects.filter().order_by('-name')
    list = {'UserList': 'UserList'}
    for object in objects:
        list[object.id] = object.name
    return list

def roomlist():
    objects = Room.objects.filter()
    list = {'RoomList': 'RoomList'}
    for object in objects:
        list[object.id] = object.name
    return list

def messagelist(id):
    objects = Message.objects.filter(room_id=id)
    name = Room.objects.get(id=id).name
    list = {'MessageList': name}
    for object in objects:
        message = {object.author.name: object.text}
        list[object.id] = message
    return list

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(json.dumps({'message': 'соединение установлено'}))
        async_to_sync(self.channel_layer.group_add)('all_instructions', self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('all_instructions', self.channel_name)

# Просмотр списка других пользователей
    def all_user(self, text_data=None):
        message = text_data
        print('order for all users:', message)
        if message['order'] == 'send_list_users':
            self.send(json.dumps(userlist()))
            print('Список пользователей отправлен')
        if message['order'] == "send_list_rooms":
            self.send(json.dumps(roomlist()))
            print('Список комнат отправлен')

    def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        print('incoming path:', self.scope['path'])
        print('incoming instructions message:', message)

        if 'load' in message:
            if message['load'] == 'users':
                self.send(json.dumps(userlist()))
                print('Список пользователей:')
            if message['load'] == 'rooms':
                self.send(json.dumps(roomlist()))
                print('Список комнат:')
            if message['load'] == 'messageList':
                self.send(json.dumps(messagelist(message['newroom_id'])))
                print('Список сообщений комнаты ID:', message['newroom_id'])

# Новый пользователь
        if 'create_user' in message:
            name = message['create_user']
            if not UserProfile.objects.filter(name=name).exists():
                user = UserProfile(name=name)
                user.save()
                print('Новый пользователь', name, 'создан')
                async_to_sync(self.channel_layer.group_send)('all_instructions', {'type': 'all_user', 'order': 'send_list_users'})
            else:
                self.send(json.dumps({'message': 'Такой пользователь уже существует'}))
                print('Такой пользователь уже существует')

# Новая комната
        if 'create_room' in message:
            name = message['create_room']
            if not Room.objects.filter(name=name).exists():
                room = Room(name=name)
                room.save()
                print('новая комната', name, 'создана')
                async_to_sync(self.channel_layer.group_send)('all_instructions', {'type': 'all_user', 'order': 'send_list_users'})
            else:
                self.send(json.dumps({'message': 'Такая комната уже существует'}))
                print('Такая комната уже существует')

# удалить пользователя
        if 'delete_user' in message:
            id = message['delete_user']
            user = UserProfile.objects.get(id=id)
            user.delete()
            print('Пользователь ID', id, 'удален')
            async_to_sync(self.channel_layer.group_send)('all_instructions', {'type': 'all_user', 'order': 'send_list_users'})

# удалить комнату
        if 'delete_room' in message:
            id = message['delete_room']
            room = Room.objects.get(id=id)
            room.delete()
            print('Комната ID', id, 'удалена')
            async_to_sync(self.channel_layer.group_send)('all_instructions', {'type': 'all_user', 'order': 'send_list_users'})

# изменить имя пользователя
        if 'order' in message:
            if message['order'] == 'changeUserName':
                id = message['id']
                name = message['name']
                if not UserProfile.objects.filter(name=name).exists():
                    user = UserProfile.objects.get(id=id)
                    user.name = name
                    user.save()
                    print('Имя пользователя ID:', id, 'изменено на:', name)
                    async_to_sync(self.channel_layer.group_send)('all_instructions', {'type': 'all_user', 'order': 'send_list_users'})
                else:
                    self.send(json.dumps({'message': 'Такой пользователь уже существует'}))
                    print('Такой пользователь уже существует')

# изменить название комнаты
            if message['order'] == 'changeRoomName':
                id = message['id']
                name = message['name']
                if not Room.objects.filter(name=name).exists():
                    room = Room.objects.get(id=id)
                    room.name = name
                    room.save()
                    print('Название комнаты ID:', id, 'изменено на:', name)
                    async_to_sync(self.channel_layer.group_send)('all_instructions', {'type': 'all_user', 'order': 'send_list_users'})
                else:
                    self.send(json.dumps({'message': 'Такая комната уже существует'}))
                    print('Такая комната уже существует')


class WSChat(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(json.dumps({'message': 'соединение c комнатой установлено'}))
        async_to_sync(self.channel_layer.group_add)('all_chat', self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('all_chat', self.channel_name)

    def incoming_message(self, text_data=None):
        message = text_data
        print('incoming message from group:', message)
        if message['order'] == 'accept_message':
            name = message['name']
            message = message['message']
            self.send(json.dumps({'message': message, 'name': name}))
            print('сообщение принято клиентом')

    def all_chats(self, text_data=None):
        message = text_data
        print('incoming message from group:', message)

    def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        print('incoming path:', self.scope["path"])
        print('incoming instructions message:', message)

        if 'usersendcommandroom' in message:
            if message['usersendcommandroom'] == 'roomselect':
                if message['oldroom_id'] != '':
                    oldroom_id = str(message['oldroom_id'])
                    async_to_sync(self.channel_layer.group_discard)(oldroom_id, self.channel_name)
                    print('Произошло отключение от комнаты', oldroom_id)
                newroom_id = str(message['newroom_id'])
                async_to_sync(self.channel_layer.group_add)(newroom_id, self.channel_name)
                print('Произошло подключение к комнате', newroom_id)

            if message['usersendcommandroom'] == 'message':
                room_id = str(message['room_id'])
                user_id = message['userid']
                username = UserProfile.objects.get(id=user_id).name
                message = message['message']
                message_save = Message(author=UserProfile.objects.get(id=user_id), room=Room.objects.get(id=room_id), text=message)
                message_save.save()
                print('Сообщение', message, 'сохранено в базе')
                async_to_sync(self.channel_layer.group_send)(room_id, {"type": "incoming_message", "order": "accept_message", "name": username, "message": message})
                print('Сообщение', message, 'отправлено в комнату', room_id)