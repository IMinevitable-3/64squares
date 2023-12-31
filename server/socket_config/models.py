from django.db import models

# Create your models here.
class Game(models.Model):
    channel_name_1 = models.CharField(max_length=255, unique=True)
    channel_name_2 = models.CharField(max_length=255, unique=True , null=True)
    gameid = models.CharField(max_length=255 , primary_key=True) 
    time  = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Channel: {self.channel_name_1}, Group: {self.gameid}, Created At: {self.time}"

class CustomGame(models.Model):
    game_id = models.CharField(max_length=255 , primary_key=True) 
    creator = models.CharField(max_length=255, unique=True)
    created_at = models.TimeField(auto_now_add=True)
    status = models.IntegerField(default=0) #  -1 - completed ,0 - idle , 1 - playing 