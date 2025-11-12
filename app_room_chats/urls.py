from django.urls import path
from . import views

app_name = 'room_chats'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<uuid:room_id>/', views.chat_room, name='chat_room'),
    path('order/<uuid:order_id>/chat/', views.create_or_get_chat, name='create_or_get_chat'),
    path('<uuid:room_id>/close/', views.close_chat, name='close_chat'),
]
