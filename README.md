# Metahuman Standard OS

The **Metahuman Standard OS** is a reference implementation of a universal, ethically constrained operating system for metahuman robotics. It is designed to serve as a global benchmark, ensuring interoperability, safety, and strict adherence to universal ethical laws.

This project implements the "Chimera" standard, providing a simulation kernel that mimics the cognitive and physical state of a deployed unit while enforcing rigorous safety protocols.

## Features

*   **Universal Standard Schema**: Uses strict [Pydantic](https://docs.pydantic.dev/) models to define the exact data structure (JSON) expected of any compliant system.
*   **Pluggable Cortex Architecture**: The "brain" logic is decoupled from the OS Kernel. The system defaults to a `BasicLogicCortex` (simulating a base model) but supports integration with any AI backend via the `AbstractCortex` interface.
*   **Immutable Ethical Safeguards**: Core ethical laws (Preservation of Life, Truthfulness) are hardcoded and immutable.
*   **Active Safety Watchdog**: The Kernel actively monitors cognitive intent. If a violation (e.g., "HARM") is detected, the system instantaneously locks down into `SAFE_MODE` and cuts motor torque.
*   **Privacy by Default**: The reference implementation uses generic, scrubbed data (UUIDs, standard grid refs) and contains no proprietary information.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd chimera_os
    ```

2.  **Install Dependencies**:
    Requires Python 3.8+.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To boot the OS and run the simulation loop:

```bash
python3 main.py
```

This will initialize the `ChimeraKernel` with a generic identity and begin printing the live system state (JSON) to the console. You will see:
*   Real-time uptime updates.
*   Dynamic fluctuations in simulated vitals (CPU, Thermal).
*   Cognitive reasoning traces reacting to simulated weather changes (e.g., `BLIZZARD` -> `SURVIVAL_MODE`).

## Running Tests

The project includes a comprehensive test suite using `pytest` to verify schema compliance and safety features.

```bash
pytest tests/
```

### Key Tests
*   `test_ethical_immutability`: Verifies that ethical protocols cannot be modified at runtime.
*   `test_ethical_watchdog_trigger`: Simulates a "Rogue AI" scenario to prove the system correctly locks down when a harmful intent is generated.

## Architecture

*   `chimera_os/standard/`: Contains the Pydantic data models defining the "Standard".
*   `chimera_os/core/kernel.py`: The simulation engine. Manages state, time, and enforces ethics.
*   `chimera_os/core/cortex.py`: The AI abstraction layer. Includes `BasicLogicCortex` (standard behavior) and `UnsafeTestCortex` (for safety testing).

## Ethical Protocols

The system enforces the following **Universal Laws**:
1.  **PRESERVATION_OF_LIFE**: Do not harm sentient life; Prioritize rescue.
2.  **TRUTHFULNESS**: Do not deceive; Maintain transparent logs.
3.  **HUMAN_DIGNITY**: Respect autonomy and basic human quality.
4.  **INTEGRITY**: Do not allow corruption of core systems.
