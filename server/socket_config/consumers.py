import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Game, CustomGame
from .generator import Generator
from channels.layers import get_channel_layer


class LobbyConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def anyWaitingPlayer(self):
        return Game.objects.filter(channel_name_2=None).count() > 0

    @database_sync_to_async
    def addPlayerToLobby(self, id, channel_name_1):
        try:
            Game.objects.create(gameid=id, channel_name_1=channel_name_1).save()
        except IntegrityError as e:
            print(f"IntegrityError: {e}")

    @database_sync_to_async
    def waitingPlayerRoom(self, channel_name_2):
        waiting_games = Game.objects.filter(channel_name_2=None)
        earliest_game = waiting_games.earliest("time")
        id = earliest_game.gameid
        updated_record = Game.objects.get(gameid=id)
        updated_record.channel_name_2 = channel_name_2
        updated_record.save()
        return id

    @database_sync_to_async
    def getGroupId(self, channel_name):
        if Game.objects.get(channel_name_1=channel_name).gameid == None:
            return Game.objects.get(channel_name_2=channel_name).gameid

    async def connect(self):
        # Get the unique channel name

        # if Any waiting player ,  pair new player with waiting player
        if await self.anyWaitingPlayer():
            id = await self.waitingPlayerRoom(self.channel_name)

            await self.channel_layer.group_add(id, self.channel_name)
            await self.send_group(id, id)

        else:
            # id = "".join([chr(random.randint(65,91)) for c in range(10)])
            id = Generator.generate_valid_group_name()
            await self.addPlayerToLobby(id, self.channel_name)
            await self.channel_layer.group_add(id, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the group when disconnected
        id = await self.getGroupId(self.channel_name)
        await self.channel_layer.group_discard(
            id, self.channel_name  # Specify the group name
        )

    async def receive(self, text_data):
        # Receive and process the incoming message

        # Broadcast the message to all clients in the group
        await self.send_group(text_data, group="some_group")

    async def send_group(self, message, group):
        # Send message to a specific group
        await self.channel_layer.group_send(
            group, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        # Receive message from group
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=message)


class GameConsumer(AsyncWebsocketConsumer):
    # Checks whether game with particular id exists
    @database_sync_to_async
    def validate_connection(self, game_id, channel_name):
        obj = Game.objects.get(gameid=game_id)
        return obj

    async def connect(self):
        path_components = self.scope["path"].strip("/").split("/")
        game_id = path_components[-1]
        exists = await self.validate_connection(game_id, self.channel_name)
        if exists:
            await self.accept()
            await self.channel_layer.group_add(game_id, self.channel_name)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle text message
        await self.send(text_data=json.dumps({"message": text_data}))

    async def send_group(self, message, group):
        await self.channel_layer.group_send(
            group, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=message)


class MyGameConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def CheckDB(self, game_id):
        try:
            return CustomGame.objects.get(game_id=game_id)
        except CustomGame.DoesNotExist:
            return None

    @database_sync_to_async
    def addDB(self, game_id, creator):
        return CustomGame.objects.create(game_id=game_id, creator=creator)

    @database_sync_to_async
    def getCreator(self, game_id):
        return CustomGame.objects.get(game_id=game_id).creator

    async def connect(self):
        path = self.scope["path"]
        game_id = path.strip("/").split("/")[-1]
        exists = await self.CheckDB(game_id)

        if exists:
            await self.accept()
            color = random.randint(0, 1)
            await self.send_group({"color": color} , game_id) #creator color assignment
            await self.send(text_data=json.dumps({"color": color^1})) #joiner color assignment
            await self.channel_layer.group_add(game_id, self.channel_name) #add  all to group
            await self.send_group({"message":"start"}, game_id)  # start game ..

        else:
            await self.accept()
            await self.channel_layer.group_add(game_id, self.channel_name)
            await self.addDB(game_id, self.channel_name)
            await self.send(text_data=json.dumps({"message": "wait"}))

    async def disconnect(self, close_code):
        # Remove the consumer from the group when disconnected
        await self.channel_layer.group_discard(
            "lyfsfked", self.channel_name  #!!!HANDLE THIS
        )

    async def receive(self, text_data):
        # Receive and process the incoming message

        # Broadcast the message to all clients in the group
        await self.send_group(text_data, group="some_group")

    async def send_group(self, message, group):
        # Send message to a specific group
        await self.channel_layer.group_send(
            group, {"type": "chat.message", "message": json.dumps(message) }
        )

    async def chat_message(self, event):
        # Receive message from group
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=message)
    