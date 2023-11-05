from django.urls import path ,re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/lobby/', consumers.LobbyConsumer.as_asgi()),
    path('ws/play/<gameid>/', consumers.GameConsumer.as_asgi()),
    path('ws/my/play/<gameid>/', consumers.MyGameConsumer.as_asgi()),


    # re_path(r'^ws/play/(?P<gameid>\w+)/$', consumers.GameConsumer.as_asgi()),
]