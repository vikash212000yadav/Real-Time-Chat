from django.conf import settings

NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS = getattr(settings, 'NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS', True)

MSG_TYPE_MESSAGE = 0
MSG_TYPE_WARNING = 1
MSG_TYPE_ALERT = 2
MSG_TYPE_MUTED = 3
MSG_TYPE_ENTER = 4
MSG_TYPE_LEAVE = 5

MESSAGE_TYPES_CHOICES = getattr(settings, 'MESSAGE_TYPES_CHOICES', (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_WARNING, 'WARNING'),
    (MSG_TYPE_ALERT, 'ALERT'),
    (MSG_TYPE_MUTED, 'MUTED'),
    (MSG_TYPE_ENTER, 'ENTER'),
    (MSG_TYPE_LEAVE, 'LEAVE')
))

MESSAGE_TYPES_LIST = getattr(settings, 'MESSAGE_TYPES_LIST',
                             [
                                 MSG_TYPE_MESSAGE,
                                 MSG_TYPE_WARNING,
                                 MSG_TYPE_ALERT,
                                 MSG_TYPE_MUTED,
                                 MSG_TYPE_ENTER,
                                 MSG_TYPE_LEAVE
                             ])
