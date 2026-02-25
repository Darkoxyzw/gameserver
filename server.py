import asyncio
import json
from aiohttp import web
import aiohttp

players = {}

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    player_id = id(ws)
    players[player_id] = ws
    print(f"Conectado: {player_id} | Total: {len(players)}")

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            data["id"] = player_id
            out = json.dumps(data)
            for pid, client in list(players.items()):
                if pid != player_id:
                    try:
                        await client.send_str(out)
                    except:
                        pass
        elif msg.type == aiohttp.WSMsgType.ERROR:
            break

    del players[player_id]
    print(f"Desconectado: {player_id} | Total: {len(players)}")
    return ws

async def health(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", websocket_handler)
app.router.add_get("/health", health)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
