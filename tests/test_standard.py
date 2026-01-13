import json
import pytest
from chimera_os.core.kernel import ChimeraKernel
from chimera_os.standard.schema import MetahumanOSState

def test_kernel_initialization():
    """Verify the kernel initializes with the correct default identity."""
    kernel = ChimeraKernel()
    assert kernel.state.system_identity.codename == "CHIMERA_PRIME"
    assert kernel.state.infrastructure_health.swarmos.status == "ACTIVE"
    assert len(kernel.state.swarm_topology.nodes) == 3

def test_standard_compliance():
    """Verify the generated JSON strictly adheres to the schema."""
    kernel = ChimeraKernel()
    json_output = kernel.get_json()

    # Parse it back to ensure it is valid JSON
    data = json.loads(json_output)

    # Validate against the Pydantic model (The Standard)
    # This ensures no field is missing or malformed
    validated_state = MetahumanOSState(**data)

    assert validated_state.system_identity.codename == "CHIMERA_PRIME"
    assert validated_state.active_mission.id == "GENESIS-01"

import time

def test_simulation_tick():
    """Verify that the tick method updates dynamic fields."""
    kernel = ChimeraKernel()
    initial_uptime = kernel.state.system_identity.uptime
    initial_timestamp = kernel.state.system_identity.timestamp

    # Sleep to ensure uptime changes (min resolution 1 second)
    time.sleep(1.1)

    # Run a tick
    kernel.tick()

    assert kernel.state.system_identity.uptime != initial_uptime
    assert kernel.state.system_identity.timestamp > initial_timestamp
    # CPU load is randomized, so it might change or stay same, but it's a float
    assert isinstance(kernel.state.infrastructure_health.vitals.cpu_load_avg, float)
