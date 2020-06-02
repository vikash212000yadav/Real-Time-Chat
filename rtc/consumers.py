import json

from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user

from rtc.exceptions import ClientError
from rtc.models import Room
from rtc.settings import NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS, MSG_TYPE_ENTER, MSG_TYPE_LEAVE
from rtc.utils import catch_client_error, get_room_or_error


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    message.channel_session['rooms'] = []


@channel_session_user
def ws_disconnect(message):
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("rtc.receive").send(payload)


@channel_session_user
@catch_client_error
def rtc_join(message):
    room = get_room_or_error(message["room"], message.user)
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_ENTER)

    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(room.id),
            "title": room.title,
        }),
    })


@channel_session_user
@catch_client_error
def rtc_leave(message):
    room = get_room_or_error(message["room"], message.user)
    if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
        room.send_message(None, message.user, MSG_TYPE_LEAVE)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(room.id),
        }),
    })


@channel_session_user
@catch_client_error
def rtc_send(message):
    if int(message['room']) not in message.channel_session['rooms']:
        raise ClientError("ROOM_ACCESS_DENIED")
    room = get_room_or_error(message["room"], message.user)
    room.send_message(message["message"], message.user)
