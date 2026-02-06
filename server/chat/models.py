import mongoengine as me
import datetime


class ChatLog(me.Document):
    user_id = me.UUIDField(required=True)
    session_id = me.StringField(required=True)
    event = me.StringField(required=True, choices=["message", "join", "leave"])
    payload = me.DictField()  # flexible JSON payload
    timestamp = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "indexes": ["user_id", "session_id", "-timestamp"],
        "ordering": ["-timestamp"],
    }
