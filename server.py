import asyncio
import http
import signal
import json
from websockets.asyncio.server import serve

players = {}

async def handler(websocket):
    player_id = id(websocket)
    players[player_id] = websocket
    print(f"Conectado: {player_id} | Total: {len(players)}")
    try:
        async for message in websocket:
            data = json.loads(message)
            data["id"] = player_id
            out = json.dumps(data)
            for pid, ws in list(players.items()):
                if pid != player_id:
                    try:
                        await ws.send(out)
                    except:
                        pass
    finally:
        del players[player_id]
        print(f"Desconectado: {player_id} | Total: {len(players)}")

def health_check(connection, request):
    if request.path == "/healthz":
        return connection.respond(http.HTTPStatus.OK, "OK\n")

async def main():
    async with serve(handler, "0.0.0.0", 8080, process_request=health_check) as server:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, server.close)
        await server.wait_closed()

asyncio.run(main())
