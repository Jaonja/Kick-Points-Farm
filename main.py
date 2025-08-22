import asyncio,json,traceback

from _webosckets.ws_token import KickPoints
from _webosckets.ws_connect import KickWebSocket

from utils.kick_utility import KickUtility
from utils.get_points_amount import PointsAmount

from loguru import logger

config = json.load(open("config.json", "r", encoding="utf-8"))

async def main():
    tasks = []
    
    for streamer in config['Streamers']:
        task = asyncio.create_task(handle_streamer(streamer))
        tasks.append(task)
    
    await asyncio.gather(*tasks)

async def check_points_periodically(streamer_name):
    while True:
        try:
            await asyncio.sleep(30)
            points_amount = PointsAmount()
            amount = points_amount.get_amount(streamer_name, config['Private']['token'])
            logger.info(f"Points amount for {streamer_name}: {amount}")
        except:
            traceback.print_exc()

async def handle_streamer(streamer_config):
    streamer_name = streamer_config['name']
    logger.info(f"Starting connection for streamer: {streamer_name}")

    try:
        kick_points = KickPoints(config['Private']['token'])
        token = kick_points.get_ws_token()
        if not token:
            logger.error(f"Failed to retrieve WebSocket token for {streamer_name}")
            return
        
        logger.info(f"WebSocket token obtained for {streamer_name}")

        kick_stream_id = KickUtility(streamer_name)
        stream_id = kick_stream_id.get_stream_id()
        channel_id = kick_stream_id.get_channel_id()

        if not stream_id or not channel_id:
            logger.error(f"Failed to get stream/channel ID for {streamer_name}")
            return

        kick_websocket_client = KickWebSocket({
            "token": token,
            "streamId": stream_id,
            "channelId": channel_id
        })

        websocket_task = asyncio.create_task(kick_websocket_client.connect())
        points_task = asyncio.create_task(check_points_periodically(streamer_name))

        await asyncio.gather(websocket_task, points_task, return_exceptions=True)
    except:
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())