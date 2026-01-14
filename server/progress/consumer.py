from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.group_name = f"progress_{self.user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        progress_update = data.get("progress", 0)

        await self.channel_layer.group_send(
            self.group_name, {"type": "progress_update", "progress": progress_update}
        )

    async def progress_update(self, event):
        await self.send(text_data=json.dumps({"progress": event["progress"]}))
