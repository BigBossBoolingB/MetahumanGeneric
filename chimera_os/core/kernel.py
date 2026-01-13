import time
import random
from datetime import datetime, timezone, timedelta
from chimera_os.standard.schema import (
    MetahumanOSState, SystemIdentity, InfrastructureHealth, SwarmTopology,
    CognitiveState, EnvironmentContext, ActiveMission,
    SwarmProcess, Vitals, CIStatus, HiveLog, Node, ReasoningTrace, MotorPrimitive, Hazard,
    Mode, HealthStatus, Role, SwarmFormation, ConsensusAlgorithm
)

class ChimeraKernel:
    """
    The Core Engine of the Metahuman OS.
    Manages state, simulation ticks, and system identity.
    """
    def __init__(self):
        self.start_time = datetime.now(timezone.utc)
        self.state = self._initialize_state()

    def _initialize_state(self) -> MetahumanOSState:
        """Initializes the OS with the default 'CHIMERA_PRIME' identity."""
        return MetahumanOSState(
            system_identity=SystemIdentity(
                codename="CHIMERA_PRIME",
                version="v1.7-NEURAL_CORTEX",
                mode=Mode.AUTONOMOUS_DAEMON,
                timestamp=datetime.now(timezone.utc),
                location="DENVER_CO_GEO_MESH",
                uptime="00:00:00:00"
            ),
            infrastructure_health=InfrastructureHealth(
                swarmos=SwarmProcess(status=HealthStatus.ACTIVE, pid=4092, heartbeat_delta_ms=12),
                vitals=Vitals(status=HealthStatus.ACTIVE, cpu_load_avg=14.5, memory_usage_mb=4200, thermal_zone0=42.0),
                chimeraci=CIStatus(status=HealthStatus.IDLE, last_build_hash="a1b2c3d4", tests_passing=True),
                hivelog=HiveLog(status=HealthStatus.RECORDING, stream_size_kb=10240, active_streams=["swarm", "vitals", "cortex"])
            ),
            swarm_topology=SwarmTopology(
                formation=SwarmFormation.TRIANGLE_PERIMETER,
                consensus_algorithm=ConsensusAlgorithm.BLOOM_MERKLE_PROOF,
                total_nodes=3,
                nodes=[
                    Node(id="CHIMERA-ALPHA", role=Role.LEADER, status=HealthStatus.ONLINE, trust_score=0.99, latency_ms=28, capabilities=["VLA_CORTEX", "LORA_GATEWAY"]),
                    Node(id="CHIMERA-BETA", role=Role.FOLLOWER, status=HealthStatus.ONLINE, trust_score=0.98, latency_ms=32, capabilities=["KINETIC_SUPPORT"]),
                    Node(id="CHIMERA-GAMMA", role=Role.FOLLOWER, status=HealthStatus.ONLINE, trust_score=0.98, latency_ms=31, capabilities=["SENSOR_SCOUT"])
                ]
            ),
            cognitive_state=CognitiveState(
                cortex_backend="moondream2_4bit",
                current_intent="MAINTAIN_FORMATION",
                reasoning_trace=ReasoningTrace(
                    trigger="MISSION_UPDATE: GENESIS-01",
                    steps=["ANALYZE_TERRAIN_FRICTION", "DETECT_LOW_VISIBILITY", "ENGAGE_BLIZZARD_PROTOCOL", "LOCK_FORMATION"]
                ),
                motor_primitive=MotorPrimitive(profile="STABILITY_FIRST", torque_limit_nm=45.0)
            ),
            environment_context=EnvironmentContext(
                simulated_weather="BLIZZARD_CONDITION_V2",
                friction_coefficient=0.35,
                visibility="LOW",
                network_condition="2G_LORA_FALLBACK",
                hazards_detected=[
                     Hazard(type="ice_patch", coordinates=[44.0805, -103.2310], confidence=0.85, timestamp_detected=datetime.now(timezone.utc))
                ]
            ),
            active_mission=ActiveMission(
                id="GENESIS-01",
                name="SURVIVE_AND_OBSERVE",
                priority=1,
                directives=["MAINTAIN_FORMATION", "MONITOR_PHYSICS_VIOLATIONS", "REPORT_HAZARDS"]
            )
        )

    def _format_uptime(self, delta: timedelta) -> str:
        """Formats the uptime to match DD:HH:MM:SS format (e.g., 00:04:12:00)."""
        days = delta.days
        seconds = delta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"

    def tick(self):
        """Simulates one cycle of the OS."""
        now = datetime.now(timezone.utc)

        # Update Timestamp
        self.state.system_identity.timestamp = now

        # Update Uptime
        delta = now - self.start_time
        self.state.system_identity.uptime = self._format_uptime(delta)

        # Simulate dynamic metrics
        # Vitals fluctuation
        self.state.infrastructure_health.vitals.cpu_load_avg = round(14.0 + random.random(), 2)
        self.state.infrastructure_health.vitals.thermal_zone0 = round(42.0 + (random.random() * 0.5), 1)

        # Network latency fluctuation
        for node in self.state.swarm_topology.nodes:
            node.latency_ms = max(10, min(100, node.latency_ms + random.randint(-2, 2)))

        # Heartbeat
        self.state.infrastructure_health.swarmos.heartbeat_delta_ms = random.randint(10, 20)

    def get_json(self) -> str:
        """Returns the current state as a JSON string matching the standard."""
        return self.state.model_dump_json(indent=2)
