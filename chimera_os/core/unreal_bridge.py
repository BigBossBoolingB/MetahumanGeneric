#!/usr/bin/env python3
"""
CHIMERA UNREAL BRIDGE
Connects the ChimeraOS Kernel to the MetahumanGeneric Avatar (UE5).
Protocol: JSON over WebSockets (LiveLink compatible).
"""

import asyncio
import websockets
import json
import logging
from typing import Dict, Any

# Configuration for local UE5 instance
UE5_URI = "ws://localhost:30020"  # Standard LiveLink port

class UnrealBridge:
    def __init__(self):
        self.running = True
        self.logger = logging.getLogger("UnrealBridge")
        self.logger.setLevel(logging.INFO)
        # Avoid adding multiple handlers if re-initialized
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - [UNREAL-BRIDGE] - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    async def stream_state(self, state_source_callback):
        """
        Main loop: Connects to UE5 and pushes state.
        state_source_callback: A function that returns the current state dict.
        """
        self.logger.info(f"Connecting to Metahuman at {UE5_URI}...")

        while self.running:
            try:
                async with websockets.connect(UE5_URI) as websocket:
                    self.logger.info("✅ LINK ESTABLISHED. Metahuman is listening.")

                    while self.running:
                        # 1. Get latest swarm state from the Kernel callback
                        raw_state = state_source_callback()

                        # 2. Transform for Metahuman Visualization
                        ue_payload = self._transform_state(raw_state)

                        # 3. Format for Metahuman (Custom Event)
                        packet = {
                            "EventName": "UpdateChimeraState",
                            "Parameters": ue_payload
                        }

                        # 4. Transmit
                        await websocket.send(json.dumps(packet))
                        await asyncio.sleep(0.033) # 30 FPS sync

            except ConnectionRefusedError:
                # Normal behavior if UE5 is not running yet
                self.logger.warning("Unreal Engine not found. Retrying in 5s...")
                await asyncio.sleep(5)
            except Exception as e:
                self.logger.error(f"Link Error: {e}")
                await asyncio.sleep(1)

    def _transform_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps OS state to visual/emotional parameters for the Avatar.
        """
        try:
            # Extract core metrics
            cognitive = state.get("cognitive_state", {})
            infra = state.get("infrastructure_health", {})
            env = state.get("environment_context", {})

            # Map Trust Score -> Facial Tension (Lower trust = Higher tension)
            nodes = state.get("swarm_topology", {}).get("nodes", [])
            trust_score = 1.0
            if nodes:
                # Assuming the first node is self/leader
                trust_score = nodes[0].get("trust_score", 1.0)

            # Map CPU Load -> Sweat/Heat Effect
            cpu_load = infra.get("vitals", {}).get("cpu_load_avg", 0)

            # Map Hazards -> HUD Alert Level (0=None, 1=Warning, 2=Critical)
            hazards = len(env.get("hazards_detected", []))

            return {
                "trust_level": float(trust_score),
                "facial_tension": 1.0 - float(trust_score),
                "cpu_stress": float(cpu_load) / 100.0,
                "hazard_count": int(hazards),
                "current_intent": cognitive.get("current_intent", "IDLE"),
                "weather_condition": env.get("simulated_weather", "CLEAR")
            }
        except Exception as e:
            self.logger.error(f"Transformation Error: {e}")
            return {"error": "Transformation Failed"}

# Standalone test
if __name__ == "__main__":
    # Mock state for testing
    def mock_state():
        return {
            "cognitive_state": {"current_intent": "TEST_LINK"},
            "infrastructure_health": {"vitals": {"cpu_load_avg": 50}},
            "environment_context": {"hazards_detected": ["ice"], "simulated_weather": "TEST_WEATHER"},
            "swarm_topology": {"nodes": [{"trust_score": 0.85}]}
        }

    bridge = UnrealBridge()
    try:
        asyncio.run(bridge.stream_state(mock_state))
    except KeyboardInterrupt:
        print("\nDisconnected.")
