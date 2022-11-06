from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/studybuddy/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # path('ws/rooms/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    # path('', consumers.ChatConsumer.as_asgi()),
    # path('ws/studybuddy/<str:user_email>/chat/rooms/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    # path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    # re_path(r'/ws/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    # path('studybuddy/<str:user_email>/chat/rooms/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/studybuddy/(?P<user_email>\w+)/chat/rooms/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]