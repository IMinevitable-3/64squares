import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Game
from .generator import Generator

class LobbyConsumer(AsyncWebsocketConsumer): 
   
    @database_sync_to_async
    def anyWaitingPlayer(self):
        return Game.objects.filter(channel_name_2=None).count() > 0

    @database_sync_to_async
    def addPlayerToLobby(self , id  , channel_name_1):
        try:
            Game.objects.create(gameid=id  , channel_name_1 =channel_name_1).save()
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
    @database_sync_to_async
    def waitingPlayerRoom(self , channel_name_2):
        waiting_games = Game.objects.filter(channel_name_2=None)
        earliest_game = waiting_games.earliest('time')
        id = earliest_game.gameid
        updated_record = Game.objects.get(gameid = id )
        updated_record.channel_name_2 = channel_name_2
        updated_record.save()
        return id 

    async def connect(self):
        # Get the unique channel name

        # if Any waiting player ,  pair new player with waiting player
        if await self.anyWaitingPlayer():
            id =await  self.waitingPlayerRoom(self.channel_name)

            await self.channel_layer.group_add(
                id,  
                self.channel_name
            )
        else :
            # id = "".join([chr(random.randint(65,91)) for c in range(10)])
            id  = Generator.generate_valid_group_name()
            await self.addPlayerToLobby(id , self.channel_name)
            await self.channel_layer.group_add(
                id,  
                self.channel_name
            )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the group when disconnected
        await self.channel_layer.group_discard(
            'some_group',  # Specify the group name
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive and process the incoming message

        # Broadcast the message to all clients in the group
        await self.send_group(text_data, group='some_group')

    async def send_group(self, message, group):
        # Send message to a specific group
        await self.channel_layer.group_send(
            group,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Receive message from group
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=message)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle text message
        await self.send(text_data=json.dumps({'message': text_data}))
