from django.urls import re_path,path

from .import consumers

websocket_urlpatterns=[
    # path('ws/sc/',consumers.ChatConsumer.as_asgi()),
    re_path(r'',consumers.ChatConsumer.as_asgi()),
    # re_path(r'test/<int:id>/',consumers.ChatConsumer.as_asgi()),
]