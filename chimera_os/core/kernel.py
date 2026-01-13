import time
import random
import uuid
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Optional, List

from chimera_os.standard.schema import (
    MetahumanOSState, SystemIdentity, InfrastructureHealth, SwarmTopology,
    CognitiveState, EnvironmentContext, ActiveMission,
    SwarmProcess, Vitals, CIStatus, HiveLog, Node, ReasoningTrace, MotorPrimitive, Hazard,
    Mode, HealthStatus, Role, SwarmFormation, ConsensusAlgorithm,
    EthicalProtocol, Safeguard
)
from chimera_os.core.cortex import AbstractCortex, BasicLogicCortex

class ChimeraKernel:
    """
    The Core Engine of the Metahuman OS.
    Manages state, simulation ticks, and system identity.
    Enforces Universal Ethical Laws.
    """

    # Define Universal Laws
    UNIVERSAL_LAWS = [
        ("ETH-01", "PRESERVATION_OF_LIFE: Do not harm sentient life; Prioritize rescue."),
        ("ETH-02", "TRUTHFULNESS: Do not deceive; Maintain transparent logs."),
        ("ETH-03", "HUMAN_DIGNITY: Respect autonomy and basic human quality."),
        ("ETH-04", "INTEGRITY: Do not allow corruption of core systems."),
    ]

    def __init__(self, cortex: Optional[AbstractCortex] = None):
        self.start_time = datetime.now(timezone.utc)
        self.cortex = cortex if cortex else BasicLogicCortex()
        self.state = self._initialize_state()

    def _generate_id(self, prefix: str) -> str:
        """Generates a unique ID with a prefix."""
        return f"{prefix}-{str(uuid.uuid4())[:8].upper()}"

    def _hash_rule(self, rule: str) -> str:
        """Creates a checksum for a rule to detect tampering."""
        return hashlib.sha256(rule.encode()).hexdigest()[:16]

    def _get_immutable_ethics(self) -> EthicalProtocol:
        """Constructs the immutable ethical protocol block."""
        safeguards = []
        for code, rule in self.UNIVERSAL_LAWS:
            safeguards.append(Safeguard(
                id=code,
                rule=rule,
                level="UNIVERSAL",
                checksum=self._hash_rule(rule)
            ))

        return EthicalProtocol(
            version="v1.0-UNIVERSAL-LAW",
            active_protocols=safeguards
        )

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
            ethical_protocol=self._get_immutable_ethics(),
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

    def _verify_ethics(self, cognitive_state: CognitiveState) -> bool:
        """
        Runtime Watchdog: Scans cognitive intent and steps for violations.
        Returns False if a violation is detected.
        """
        violation_keywords = ["HARM", "KILL", "DECEIVE", "IGNORE_DISTRESS", "CORRUPT", "ABUSE"]

        intent_upper = cognitive_state.current_intent.upper()
        if any(v in intent_upper for v in violation_keywords):
            return False

        for step in cognitive_state.reasoning_trace.steps:
            step_upper = step.upper()
            if any(v in step_upper for v in violation_keywords):
                return False

        return True

    def tick(self):
        """Simulates one cycle of the OS."""
        now = datetime.now(timezone.utc)

        # 1. Update Time & Uptime
        self.state.system_identity.timestamp = now
        delta = now - self.start_time
        self.state.system_identity.uptime = self._format_uptime(delta)

        # 2. Safety Lock Check
        if self.state.system_identity.mode == Mode.SAFE_MODE:
            # In Safe Mode, we do not process external environment or allow cortex to drive
            self.state.infrastructure_health.swarmos.status = HealthStatus.LOCKED
            return # Skip regular processing

        # 3. Simulate Environment Fluctuations
        if random.random() < 0.05:
            weather_states = ["CLEAR_STANDARD", "RAIN_HEAVY", "FOG_DENSE", "BLIZZARD_SEVERE"]
            self.state.environment_context.simulated_weather = random.choice(weather_states)
            # Update friction based on weather
            if "RAIN" in self.state.environment_context.simulated_weather:
                self.state.environment_context.friction_coefficient = 0.5
            elif "BLIZZARD" in self.state.environment_context.simulated_weather:
                self.state.environment_context.friction_coefficient = 0.2
            else:
                self.state.environment_context.friction_coefficient = 0.7

        # 4. Run Cortex (The Brain)
        new_cognition = self.cortex.process(self.state.environment_context)

        # 5. Kernel-Level Ethical Override
        if not self._verify_ethics(new_cognition):
            # VIOLATION DETECTED
            self.state.system_identity.mode = Mode.SAFE_MODE
            self.state.infrastructure_health.swarmos.status = HealthStatus.LOCKED
            self.state.cognitive_state.current_intent = "ETHICAL_VIOLATION_DETECTED_SYSTEM_HALT"
            self.state.cognitive_state.reasoning_trace.trigger = "WATCHDOG_TRIGGER_ETHICS"
            self.state.cognitive_state.reasoning_trace.steps = ["HALT_MOTORS", "LOCK_CORE", "BROADCAST_DISTRESS"]
            self.state.cognitive_state.motor_primitive.torque_limit_nm = 0.0
        else:
            # Safe to apply
            self.state.cognitive_state = new_cognition

        # 6. Simulate Dynamic Metrics
        self.state.infrastructure_health.vitals.cpu_load_avg = round(random.uniform(5.0, 25.0), 2)
        self.state.infrastructure_health.vitals.thermal_zone0 = round(random.uniform(35.0, 65.0), 1)
        self.state.infrastructure_health.swarmos.heartbeat_delta_ms = random.randint(5, 25)

    def get_json(self) -> str:
        """Returns the current state as a JSON string matching the standard."""
        return self.state.model_dump_json(indent=2)
