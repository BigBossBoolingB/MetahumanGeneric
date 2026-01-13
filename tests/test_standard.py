import json
import time
import pytest
from chimera_os.core.kernel import ChimeraKernel
from chimera_os.standard.schema import MetahumanOSState, EnvironmentContext

def test_kernel_initialization_generic():
    """Verify the kernel initializes with generic data, not hardcoded proprietary strings."""
    kernel = ChimeraKernel()

    # Check that identity is generated (starts with UNIT-)
    assert kernel.state.system_identity.codename.startswith("UNIT-")
    # Check that it is NOT the specific hardcoded value from the prompt
    assert kernel.state.system_identity.codename != "CHIMERA_PRIME"

    # Check location is generic
    assert "DENVER" not in kernel.state.system_identity.location
    assert kernel.state.system_identity.location == "GLOBAL_GRID_STANDARD_REF"

def test_standard_compliance():
    """Verify the generated JSON strictly adheres to the schema."""
    kernel = ChimeraKernel()
    json_output = kernel.get_json()
    data = json.loads(json_output)
    validated_state = MetahumanOSState(**data)

    assert validated_state.system_identity.version == "v2.0-STANDARD-CORE"

def test_cortex_logic_integration():
    """Verify that the cortex updates the cognitive state based on environment."""
    kernel = ChimeraKernel()

    # Force a specific environment condition
    kernel.state.environment_context.simulated_weather = "BLIZZARD_SEVERE"
    kernel.state.environment_context.friction_coefficient = 0.2

    # Run tick to trigger cortex processing
    kernel.tick()

    # The BasicLogicCortex should detect the blizzard and update intent
    assert kernel.state.cognitive_state.current_intent == "SURVIVAL_MODE"
    assert "WEATHER_ALERT" in kernel.state.cognitive_state.reasoning_trace.trigger
    assert "INCREASE_GRIP" in kernel.state.cognitive_state.reasoning_trace.steps

def test_simulation_tick_dynamic():
    """Verify that the tick method updates dynamic fields."""
    kernel = ChimeraKernel()
    initial_uptime = kernel.state.system_identity.uptime
    initial_timestamp = kernel.state.system_identity.timestamp

    # Sleep to ensure uptime changes
    time.sleep(1.1)

    kernel.tick()

    assert kernel.state.system_identity.uptime != initial_uptime
    assert kernel.state.system_identity.timestamp > initial_timestamp
