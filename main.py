import time
import sys
from chimera_os.core.kernel import ChimeraKernel

def boot_sequence():
    print("Initializing CHIMERA_PRIME OS...")
    kernel = ChimeraKernel()
    print(f"Kernel Loaded: {kernel.state.system_identity.version}")
    print("Entering AUTONOMOUS_DAEMON mode...")
    print("-" * 50)

    try:
        while True:
            kernel.tick()

            # Clear screen (ANSI escape code) and print state
            # In a real log system we wouldn't clear screen, but for a "dashboard" simulation we might.
            # For this task, let's just print the state every few seconds to show it changing.
            print(f"\n--- OS STATE SNAPSHOT [{kernel.state.system_identity.timestamp}] ---")
            print(kernel.get_json())

            time.sleep(2)
    except KeyboardInterrupt:
        print("\nShutdown sequence initiated...")
        sys.exit(0)

if __name__ == "__main__":
    boot_sequence()
