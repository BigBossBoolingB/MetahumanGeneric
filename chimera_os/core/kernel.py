import time
import random
import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

from chimera_os.standard.schema import (
    MetahumanOSState, SystemIdentity, InfrastructureHealth, SwarmTopology,
    CognitiveState, EnvironmentContext, ActiveMission,
    SwarmProcess, Vitals, CIStatus, HiveLog, Node, ReasoningTrace, MotorPrimitive, Hazard,
    Mode, HealthStatus, Role, SwarmFormation, ConsensusAlgorithm
)
from chimera_os.core.cortex import AbstractCortex, BasicLogicCortex

class ChimeraKernel:
    """
    The Core Engine of the Metahuman OS.
    Manages state, simulation ticks, and system identity.
    """
    def __init__(self, cortex: Optional[AbstractCortex] = None):
        self.start_time = datetime.now(timezone.utc)
        self.cortex = cortex if cortex else BasicLogicCortex()
        self.state = self._initialize_state()

    def _generate_id(self, prefix: str) -> str:
        """Generates a unique ID with a prefix."""
        return f"{prefix}-{str(uuid.uuid4())[:8].upper()}"

    def _initialize_state(self) -> MetahumanOSState:
        """
        Initializes the OS with a generic Standard Identity.
        No proprietary data is used.
        """
        sys_id = self._generate_id("UNIT")

        # Generic Environment Context
        initial_env = EnvironmentContext(
            simulated_weather="CLEAR_STANDARD",
            friction_coefficient=0.7,
            visibility="HIGH",
            network_condition="5G_MESH_STANDARD",
            hazards_detected=[]
        )

        # Initial Cognitive Pass
        initial_cognition = self.cortex.process(initial_env)

        return MetahumanOSState(
            system_identity=SystemIdentity(
                codename=sys_id,
                version="v2.0-STANDARD-CORE",
                mode=Mode.AUTONOMOUS_DAEMON,
                timestamp=datetime.now(timezone.utc),
                location="GLOBAL_GRID_STANDARD_REF",
                uptime="00:00:00:00"
            ),
            infrastructure_health=InfrastructureHealth(
                swarmos=SwarmProcess(status=HealthStatus.ACTIVE, pid=random.randint(1000, 9999), heartbeat_delta_ms=10),
                vitals=Vitals(status=HealthStatus.ACTIVE, cpu_load_avg=5.0, memory_usage_mb=1024, thermal_zone0=35.0),
                chimeraci=CIStatus(status=HealthStatus.IDLE, last_build_hash="00000000", tests_passing=True),
                hivelog=HiveLog(status=HealthStatus.RECORDING, stream_size_kb=0, active_streams=["system", "security"])
            ),
            swarm_topology=SwarmTopology(
                formation=SwarmFormation.LINE,
                consensus_algorithm=ConsensusAlgorithm.RAFT,
                total_nodes=1,
                nodes=[
                    Node(
                        id=sys_id,
                        role=Role.LEADER,
                        status=HealthStatus.ONLINE,
                        trust_score=1.0,
                        latency_ms=0,
                        capabilities=["STANDARD_COMPUTE", "STANDARD_SENSORS"]
                    )
                ]
            ),
            cognitive_state=initial_cognition,
            environment_context=initial_env,
            active_mission=ActiveMission(
                id=self._generate_id("MISSION"),
                name="STANDARD_OPERATING_PROCEDURE",
                priority=3,
                directives=["STANDBY", "SELF_DIAGNOSE"]
            )
        )

    def _format_uptime(self, delta: timedelta) -> str:
        """Formats the uptime to match DD:HH:MM:SS format."""
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"

    def tick(self):
        """Simulates one cycle of the OS."""
        now = datetime.now(timezone.utc)

        # 1. Update Time & Uptime
        self.state.system_identity.timestamp = now
        delta = now - self.start_time
        self.state.system_identity.uptime = self._format_uptime(delta)

        # 2. Simulate Environment Fluctuations (Random Walk)
        # Randomly change weather occasionally to trigger Cortex
        if random.random() < 0.05:
            weather_states = ["CLEAR_STANDARD", "RAIN_HEAVY", "FOG_DENSE", "BLIZZARD_SEVERE"]
            self.state.environment_context.simulated_weather = random.choice(weather_states)
            if "RAIN" in self.state.environment_context.simulated_weather:
                self.state.environment_context.friction_coefficient = 0.5
            elif "BLIZZARD" in self.state.environment_context.simulated_weather:
                self.state.environment_context.friction_coefficient = 0.2
            else:
                self.state.environment_context.friction_coefficient = 0.7

        # 3. Run Cortex (The Brain)
        # The cortex decides the intent based on the updated environment
        new_cognition = self.cortex.process(self.state.environment_context)
        self.state.cognitive_state = new_cognition

        # 4. Simulate Dynamic Metrics
        self.state.infrastructure_health.vitals.cpu_load_avg = round(random.uniform(5.0, 25.0), 2)
        self.state.infrastructure_health.vitals.thermal_zone0 = round(random.uniform(35.0, 65.0), 1)
        self.state.infrastructure_health.swarmos.heartbeat_delta_ms = random.randint(5, 25)

    def get_json(self) -> str:
        """Returns the current state as a JSON string matching the standard."""
        return self.state.model_dump_json(indent=2)
