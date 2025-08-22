import rnet,json,asyncio,traceback

from typing import Dict, Optional
from dataclasses import dataclass
from rnet import WebSocket, Message
from loguru import logger

@dataclass
class ConnectionState:
    is_connected: bool = False
    reconnect_attempts: int = 0
    max_reconnect_attempts: int = 5

class KickWebSocket:
    def __init__(self, data: Dict[str, str]):
        self.ws: Optional[WebSocket] = None
        self.data = data
        self.state = ConnectionState()
        self.handshake_task: Optional[asyncio.Task] = None
        self.tracking_task: Optional[asyncio.Task] = None
        self._running = False

    async def connect(self) -> bool:
        if not self.data["token"]:
            logger.error("Token must not be empty")
            return False

        try:
            self.ws = await rnet.websocket(
                url=f"wss://websockets.kick.com/viewer/v1/connect?token={self.data['token']}",
                read_buffer_size=1024,
                write_buffer_size=1024,
                max_message_size=1024
            )
            
            logger.success(f"[+] WebSocket connected successfully")
            self.state.is_connected = True
            self.state.reconnect_attempts = 0
            
            await self._send_initial_messages()
            await self._start_background_tasks()
            await self._listen_for_messages()
            
            return True
            
        except:
            traceback.print_exc()
            self.state.is_connected = False
            await self._handle_reconnection()
            return False

    async def _send_initial_messages(self):
        await self._send_handshake()
        await self._send_ping()

    async def _start_background_tasks(self):
        self._running = True
        
        self.handshake_task = asyncio.create_task(self._handshake_loop())
        self.tracking_task = asyncio.create_task(self._tracking_loop())

    async def _handshake_loop(self):
        while self._running and self.state.is_connected:
            try:
                await asyncio.sleep(30)
                if self.state.is_connected:
                    await self._send_handshake()
                    await self._send_ping()
            except:
                traceback.print_exc()
                break

    async def _tracking_loop(self):
        while self._running and self.state.is_connected:
            try:
                await asyncio.sleep(10)
                if self.state.is_connected:
                    await self._send_user_event()
            except:
                traceback.print_exc()
                break

    async def _listen_for_messages(self):
        try:
            while self.state.is_connected and self._running:
                message = await self.ws.recv()
                await self._handle_message(message)
        except:
            traceback.print_exc()
            self.state.is_connected = False
            await self._handle_reconnection()

    async def _handle_message(self, message):
        try:
            if not hasattr(message, 'text'):
                message_str = message.text
            else:
                message_str = str(message)

            if message_str == "ping":
                await self._send_pong()
                logger.info("[+] Raw ping received, sending pong")
                return

            parsed_message = json.loads(message_str)
            message_type = parsed_message["type"]

            match message_type:
                case "channel_handshake":
                    channel_id = parsed_message["data"]["message"]["channelId"]
                    logger.info(f"[+] Channel handshake received: channelId={channel_id}")
                
                case "ping":
                    await self._send_pong()
                    logger.info("[+] Ping received, sending pong")
                
                case "pong":
                    logger.info("[+] Pong received")
                
                case _:
                    logger.info(f"[+] Message received: {message_str}")

        except:
            traceback.print_exc()

    async def _handle_reconnection(self):
        if self.state.reconnect_attempts < self.state.max_reconnect_attempts:
            self.state.reconnect_attempts += 1
            logger.info(f"[+] Attempting to reconnect ({self.state.reconnect_attempts}/{self.state.max_reconnect_attempts})...")
            
            await self._cleanup_tasks()
            await asyncio.sleep(5)
            await self.connect()
        else:
            logger.error("[-] Max reconnection attempts reached")
            await self.disconnect()

    async def _cleanup_tasks(self):
        self._running = False
        
        if self.handshake_task and not self.handshake_task.done():
            self.handshake_task.cancel()
            
        if self.tracking_task and not self.tracking_task.done():
            self.tracking_task.cancel()

    async def disconnect(self):
        logger.info("[-] WebSocket connection closed")
        self.state.is_connected = False
        await self._cleanup_tasks()
        
        if self.ws:
            await self.ws.close()

    async def _send_handshake(self):
        if not self.state.is_connected:
            return
            
        payload = {
            "type": "channel_handshake",
            "data": {
                "message": {
                    "channelId": int(self.data["channelId"]),
                }
            }
        }

        try:
            await self.ws.send(Message.from_text(json.dumps(payload)))
            logger.debug(f"Sent handshake for channel ID: {self.data['channelId']}")
        except:
            traceback.print_exc()
            self.state.is_connected = False

    async def _send_ping(self):
        if not self.state.is_connected:
            return
            
        payload = {"type": "ping"}

        try:
            await self.ws.send(Message.from_text(json.dumps(payload)))
            logger.debug("Sent ping message")
        except:
            traceback.print_exc()
            self.state.is_connected = False

    async def _send_pong(self):
        if not self.state.is_connected:
            return
            
        payload = {
            "type": "pong"
        }

        try:
            await self.ws.send(Message.from_text(json.dumps(payload)))
            logger.debug("Sent pong message")
        except:
            traceback.print_exc()

    async def _send_user_event(self):
        if not self.state.is_connected:
            return
            
        payload = {
            "type": "user_event",
            "data": {
                "message": {
                    "name": "tracking.user.watch.livestream",
                    "channel_id": int(self.data["channelId"]),
                    "livestream_id": int(self.data["streamId"]),
                }
            }
        }

        try:
            await self.ws.send(Message.from_text(json.dumps(payload)))
            logger.debug(f"Sent user event for channel ID: {self.data['channelId']} and stream ID: {self.data['streamId']}")
        except:
            traceback.print_exc()
            self.state.is_connected = False
