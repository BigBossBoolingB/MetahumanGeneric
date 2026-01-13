#!/usr/bin/env python3
import asyncio
import logging
from chimera_os.core.kernel import ChimeraKernel
from chimera_os.core.unreal_bridge import UnrealBridge

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def run_kernel_loop(kernel: ChimeraKernel):
    """Runs the kernel simulation loop asynchronously"""
    while True:
        kernel.tick()
        # In a real app, tick() might be async or we sleep here to yield control
        # We print less frequently to avoid console spam, but the state updates internally
        if kernel.state.system_identity.timestamp.second % 5 == 0:
             print(f"\n[{kernel.state.system_identity.timestamp}] OS HEARTBEAT | Intent: {kernel.state.cognitive_state.current_intent}")

        await asyncio.sleep(1.0)

def get_kernel_state_callback(kernel: ChimeraKernel):
    """Helper to extract state for the bridge"""
    # The kernel.state is a Pydantic model, dump to dict
    return kernel.state.model_dump(mode='json')

async def main():
    print("------------------------------------------------")
    print("   METAHUMAN STANDARD OS (CHIMERA) - BOOTING    ")
    print("------------------------------------------------")

    # 1. Initialize Kernel
    kernel = ChimeraKernel()
    print(f"KERNEL: ONLINE | ID: {kernel.state.system_identity.codename}")
    print(f"ETHICS: ENFORCED | MODE: {kernel.state.system_identity.mode}")

    # 2. Initialize Bridge
    bridge = UnrealBridge()

    # 3. Create Tasks
    # We run the kernel tick loop and the bridge stream loop concurrently
    kernel_task = asyncio.create_task(run_kernel_loop(kernel))

    # Pass a lambda/function that grabs the *current* state whenever the bridge asks
    bridge_task = asyncio.create_task(
        bridge.stream_state(lambda: get_kernel_state_callback(kernel))
    )

    # 4. Wait
    try:
        await asyncio.gather(kernel_task, bridge_task)
    except asyncio.CancelledError:
        print("Tasks cancelled.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down ChimeraOS...")
