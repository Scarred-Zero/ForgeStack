from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CourseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope["url_route"]["kwargs"]["course_id"]
        self.group_name = f"course_{self.course_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action", "")
        payload = data.get("payload", {})

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
