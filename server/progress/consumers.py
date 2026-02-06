from channels.generic.websocket import AsyncWebsocketConsumer
import json, datetime
from logs.mongo_schema.models import ActivityLog


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"progress_{self.user_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        ActivityLog(
            user_id=self.user_id,
            session_id=self.user_id,
            event="progress",
            payload={"action": "connect"},
            timestamp=datetime.datetime.utcnow(),
        ).save()

    async def receive(self, text_data):
        data = json.loads(text_data)
        progress_update = data.get("progress", 0)

        ActivityLog(
            user_id=self.user_id,
            session_id=self.user_id,
            event="progress",
            payload={"progress": progress_update},
            timestamp=datetime.datetime.utcnow(),
        ).save()

        await self.channel_layer.group_send(
            self.group_name, {"type": "progress_update", "progress": progress_update}
        )

    async def progress_update(self, event):
        await self.send(text_data=json.dumps({"progress": event["progress"]}))
