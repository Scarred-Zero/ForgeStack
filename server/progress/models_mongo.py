import mongoengine as me
import datetime


class ProgressLog(me.Document):
    user_id = me.UUIDField(required=True)
    course_id = me.UUIDField(required=True)
    progress = me.IntField(min_value=0, max_value=100)
    timestamp = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "indexes": ["user_id", "course_id", "-timestamp"],
        "ordering": ["-timestamp"],
    }
