from datetime import datetime
import json
from app.models import Room, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    @async_to_sync
    def get_room(self, room):
        return Room.objects.get(room_name=room)
    
    @async_to_sync
    def get_room_members(self, room):
        room_members = {}
        members = Room.objects.get(room_name=room).members.all()
        for member in members:
            room.members.update({member.id: member.username})
        return room_members
    
    @async_to_sync
    def get_room_owner(self, room):
        return Room.objects.get(room_name=room).owner

    async def connect(self):
        print(f'connect: ')
        print()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print(f'receive: {text_data}')
        print()
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'sender': sender
        })

    async def chat_message(self, event):
        print(f'chat_message - event: {event}')
        print()
        message = event['message']
        sender = event['sender']
        room_name = self.scope['url_route']['kwargs']['room_name']
        print(f'chat_message, room_name: {room_name}')
        room = await self.get_room(room_name)
        room_owner = await self.get_room_owner(room_name)
        room_members = await self.get_room_members(room_name)
        print(f'new_msg: {message}')

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender,
            'room_id': room.id,
            'room_name': room_name,
            'room_owner_id': room_owner.id,
            'room_members': room_members,
        }))
