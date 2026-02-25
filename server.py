import asyncio
import websockets
import json
from http.server import BaseHTTPRequestHandler
import threading
from http.server import HTTPServer

players = {}

async def handler(websocket):
    player_id = id(websocket)
    players[player_id] = websocket
    print(f"Jogador conectado: {player_id} | Total: {len(players)}")

    try:
        async for message in websocket:
            data = json.loads(message)
            data["id"] = player_id
            msg = json.dumps(data)

            for pid, ws in list(players.items()):
                if pid != player_id:
                    try:
                        await ws.send(msg)
                    except:
                        pass
    finally:
        del players[player_id]
        print(f"Jogador desconectado: {player_id} | Total: {len(players)}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8080):
        print("Servidor rodando na porta 8080")
        await asyncio.Future()

asyncio.run(main())
