import mongoengine as me
import datetime


class ActivityLog(me.Document):
    user_id = me.StringField(required=True)
    action = me.StringField(required=True)
    metadata = me.DictField()
    ip_address = me.StringField()
    timestamp = me.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        "collection": "activity_logs",
        "indexes": [
            {"fields": ["user_id", "action"]},
            "metadata.course_id",
            "-timestamp",
        ],
        "ordering": ["-timestamp"],
    }
