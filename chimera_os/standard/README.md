# Metahuman Standard Schema

This directory contains the **Universal Standard** definition for the Metahuman OS state. It is the "source of truth" for data interoperability across all compliant units.

## Core Components

The state is defined in `schema.py` using strictly typed Pydantic models.

### `MetahumanOSState`
The root object containing all subsystems:
*   `system_identity`: Static ID, version, and dynamic uptime/timestamp.
*   `ethical_protocol`: **Immutable** list of active safeguards.
*   `infrastructure_health`: Vitals, process status, and hardware logs.
*   `swarm_topology`: Information about the unit's role in the local mesh network.
*   `cognitive_state`: The current intent, reasoning trace, and motor primitives derived from the Cortex.
*   `environment_context`: Sensor data regarding weather, friction, and hazards.

### Enums & Strict Typing
To ensure standardization, the following Enums are enforced:

*   **`Mode`**: `AUTONOMOUS_DAEMON`, `MANUAL_OVERRIDE`, `SLEEP_MODE`, `SAFE_MODE`.
*   **`Role`**: `LEADER`, `FOLLOWER`.
*   **`HealthStatus`**: `ACTIVE`, `IDLE`, `CRITICAL`, `OFFLINE`, `LOCKED`.
*   **`SwarmFormation`**: `TRIANGLE_PERIMETER`, `LINE`, `DIAMOND`.

## Immutability

The `EthicalProtocol` model is configured with `frozen=True`. This means that once the OS Kernel initializes the safeguards, they cannot be modified, deleted, or overwritten by any process (including the Cortex) during runtime.

### Protocol Structure
Each safeguard consists of:
*   `id`: Unique Code (e.g., `ETH-01`).
*   `rule`: Human-readable description of the law.
*   `level`: Scope of application (`UNIVERSAL` or `OPERATIONAL`).
*   `checksum`: A cryptographic hash of the rule text to verify integrity.
