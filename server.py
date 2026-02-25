from aiohttp import web, WSMsgType
import json

players = {}

async def ws_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    pid = id(ws)
    players[pid] = ws
    print(f"Conectado: {pid}")
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            data = json.loads(msg.data)
            data["id"] = pid
            out = json.dumps(data)
            for k, client in list(players.items()):
                if k != pid:
                    try:
                        await client.send_str(out)
                    except:
                        pass
    del players[pid]
    print(f"Desconectado: {pid}")
    return ws

async def health(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get("/", ws_handler)
app.router.add_get("/health", health)

web.run_app(app, host="0.0.0.0", port=8080)
