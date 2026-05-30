#!/usr/bin/env python
import django
import asyncio, os, sys
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from sesame.utils import get_user
from websockets.asyncio.server import ServerConnection, serve
from websockets.frames import CloseCode


async def handler(websocket):
    sesame = await websocket.recv()
    user = await asyncio.to_thread(get_user, sesame)
    if user is None:
        await websocket.close(CloseCode.INTERNAL_ERROR, "authentication failed")
        return

    await websocket.send(f"Hello {user}!")


async def main():
    async with serve(handler, "localhost", 8888):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())