from channels.generic.websocket import AsyncWebsocketConsumer
import json, datetime
from logs.mongo_schema.models import ActivityLog


class CourseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope["url_route"]["kwargs"]["course_id"]
        self.group_name = f"course_{self.course_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        ActivityLog(
            user_id=(
                self.scope["user"].id if self.scope["user"].is_authenticated else None
            ),
            session_id=self.course_id,
            event="course",
            payload={"action": "connect"},
            timestamp=datetime.datetime.utcnow(),
        ).save()

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action", "")
        payload = data.get("payload", {})

        ActivityLog(
            user_id=(
                self.scope["user"].id if self.scope["user"].is_authenticated else None
            ),
            session_id=self.course_id,
            event="course",
            payload={"action": action, "payload": payload},
            timestamp=datetime.datetime.utcnow(),
        ).save()

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "course_event", "action": action, "payload": payload},
        )

    async def course_event(self, event):
        await self.send(
            text_data=json.dumps(
                {"action": event["action"], "payload": event["payload"]}
            )
        )
