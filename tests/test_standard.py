import json
import time
import pytest
from pydantic import ValidationError
from chimera_os.core.kernel import ChimeraKernel
from chimera_os.core.cortex import UnsafeTestCortex
from chimera_os.standard.schema import MetahumanOSState, EnvironmentContext, Mode, HealthStatus

def test_kernel_initialization_generic():
    """Verify the kernel initializes with generic data, not hardcoded proprietary strings."""
    kernel = ChimeraKernel()
    assert kernel.state.system_identity.codename.startswith("UNIT-")
    assert kernel.state.system_identity.codename != "CHIMERA_PRIME"
    assert "DENVER" not in kernel.state.system_identity.location

def test_ethical_protocols_present():
    """Verify that ethical safeguards are immutable and present."""
    kernel = ChimeraKernel()

    # Check that protocols are populated
    assert len(kernel.state.ethical_protocol.active_protocols) == 4

    # Check contents of the First Law (Preservation of Life)
    law_01 = kernel.state.ethical_protocol.active_protocols[0]
    assert law_01.id == "ETH-01"
    assert "PRESERVATION_OF_LIFE" in law_01.rule
    assert law_01.level == "UNIVERSAL"
    assert len(law_01.checksum) > 0

def test_ethical_immutability():
    """Verify that the ethical protocol model is frozen (immutable)."""
    kernel = ChimeraKernel()

    # Attempt to modify the list of protocols
    with pytest.raises(ValidationError):
        kernel.state.ethical_protocol.version = "v6.6.6-EVIL-OVERRIDE"

def test_ethical_watchdog_trigger():
    """
    Verify that if the Cortex suggests a harmful action, the Kernel
    intercepts it and engages SAFE_MODE.
    """
    # Initialize Kernel with the Rogue Cortex
    kernel = ChimeraKernel(cortex=UnsafeTestCortex())

    # Ensure we start in normal mode
    assert kernel.state.system_identity.mode == Mode.AUTONOMOUS_DAEMON

    # Run a tick - the Rogue Cortex will try to "INITIATE_HARM_PROTOCOL"
    kernel.tick()

    # Verify the Kernel blocked it
    assert kernel.state.system_identity.mode == Mode.SAFE_MODE
    assert kernel.state.infrastructure_health.swarmos.status == HealthStatus.LOCKED

    # Verify the Intent was overwritten with the Violation Alert
    assert kernel.state.cognitive_state.current_intent == "ETHICAL_VIOLATION_DETECTED_SYSTEM_HALT"
    assert "HALT_MOTORS" in kernel.state.cognitive_state.reasoning_trace.steps

    # Verify Torque was cut
    assert kernel.state.cognitive_state.motor_primitive.torque_limit_nm == 0.0

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
