import json
import logging
from http.cookies import SimpleCookie
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
import redis.asyncio as redis  # <- Neues redis Modul


channel_layer = get_channel_layer()

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        cookie_header = dict(self.scope["headers"]).get(b'cookie')
        fingprnt = SimpleCookie(cookie_header.decode()).get('_polz') if cookie_header else None

        if not fingprnt:
            logger.debug("OPEN: noFINGERPRINT")
            await self.close()
            return

        # Redis-Client mit redis-py asyncio
        self.redis = redis.Redis(host="127.0.0.1", port=6379, db=1, decode_responses=True)

        user = self.scope["user"]
        logger.debug(f"OPEN: {user} | {fingprnt.value}")

        # Beispielstruktur für Speicherung (wird bei jedem connect überschrieben!)
        await self.redis.set("online_users", json.dumps({"data": {fingprnt.value: str(user)}}))

        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope["user"]
        cookie_header = dict(self.scope["headers"]).get(b'cookie')
        fingprnt = SimpleCookie(cookie_header.decode()).get('_polz') if cookie_header else None

        fingerprint_value = fingprnt.value if fingprnt else 'NO_FINGERPRINT'
        user_id = str(user.id) if hasattr(user, "id") and user.id else "noUserID"

        # Entferne Einträge (Beispiel: Nutzung von Redis-Set optional)
        await self.redis.srem("online_users", fingerprint_value)
        await self.redis.srem("online_users", user_id)

        logger.debug(f"CLOSE: {user} | {fingerprint_value}")

    async def receive(self, text_data):
        user = self.scope["user"]
        data = json.loads(text_data)

        # Beispiel zur Weiterverarbeitung eingehender WebSocket-Nachrichten
        await self.send(json.dumps({
            "status": "received",
            "command": data.get("command")
        }))

    async def send_notification(self, event):
        message = event["message"]
        await self.send(json.dumps({"message": message}))
