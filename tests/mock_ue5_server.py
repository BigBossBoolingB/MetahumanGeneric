#!/usr/bin/env python3
"""
MOCK UNREAL ENGINE SERVER
Simulates the LiveLink WebSocket receiver to verify ChimeraOS output.
"""

import asyncio
import websockets
import json
import logging
import sys

logging.basicConfig(level=logging.INFO, format='[MOCK-UE5] %(message)s')

async def handler(websocket):
    logging.info("🔌 CLIENT CONNECTED (ChimeraOS detected)")
    try:
        async for message in websocket:
            data = json.loads(message)
            event = data.get("EventName")
            params = data.get("Parameters", {})

            # Visualizing the heartbeat
            trust = params.get("trust_level", "?")
            intent = params.get("current_intent", "UNKNOWN")

            # Use sys.stdout.write/flush for immediate output capture in the bash environment
            print(f"   📨 RECV: [{event}] Intent='{intent}' Trust={trust}")
            sys.stdout.flush()

    except websockets.exceptions.ConnectionClosed:
        logging.info("🔌 CLIENT DISCONNECTED")

async def main():
    logging.info("LISTENING on ws://localhost:30020...")
    async with websockets.serve(handler, "localhost", 30020):
        await asyncio.get_running_loop().create_future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
