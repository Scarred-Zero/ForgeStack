from channels.generic.websocket import AsyncWebsocketConsumer
import json
from logs.mongo_schema.models import ActivityLog
import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Log connection event
        ActivityLog(
            user_id=(
                self.scope["user"].id if self.scope["user"].is_authenticated else None
            ),
            session_id=self.room_name,
            event="chat",
            payload={"action": "connect"},
            timestamp=datetime.datetime.utcnow(),
        ).save()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Log disconnect event
        ActivityLog(
            user_id=(
                self.scope["user"].id if self.scope["user"].is_authenticated else None
            ),
            session_id=self.room_name,
            event="chat",
            payload={"action": "disconnect"},
            timestamp=datetime.datetime.utcnow(),
        ).save()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")

        # Log message event
        ActivityLog(
            user_id=(
                self.scope["user"].id if self.scope["user"].is_authenticated else None
            ),
            session_id=self.room_name,
            event="chat",
            payload={"message": message},
            timestamp=datetime.datetime.utcnow(),
        ).save()

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
