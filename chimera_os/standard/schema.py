from __future__ import annotations
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

# Enums and Types for Standardization
class Mode(str, Enum):
    AUTONOMOUS_DAEMON = "AUTONOMOUS_DAEMON"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"
    SLEEP_MODE = "SLEEP_MODE"

class HealthStatus(str, Enum):
    ACTIVE = "ACTIVE"
    IDLE = "IDLE"
    RECORDING = "RECORDING"
    CRITICAL = "CRITICAL"
    OFFLINE = "OFFLINE"
    ONLINE = "ONLINE"

class Role(str, Enum):
    LEADER = "LEADER"
    FOLLOWER = "FOLLOWER"

class SwarmFormation(str, Enum):
    TRIANGLE_PERIMETER = "TRIANGLE_PERIMETER"
    DIAMOND = "DIAMOND"
    LINE = "LINE"

class ConsensusAlgorithm(str, Enum):
    BLOOM_MERKLE_PROOF = "BLOOM_MERKLE_PROOF"
    RAFT = "RAFT"
    PAXOS = "PAXOS"

class SystemIdentity(BaseModel):
    codename: str = Field(..., description="Unique system identifier codename")
    version: str = Field(..., description="OS Version string")
    mode: Mode = Field(..., description="Current operational mode")
    timestamp: datetime = Field(..., description="Current ISO 8601 timestamp")
    location: str = Field(..., description="Geo-location identifier")
    uptime: str = Field(..., description="System uptime in DD:HH:MM:SS format")

class SwarmProcess(BaseModel):
    status: HealthStatus
    pid: int
    heartbeat_delta_ms: int

class Vitals(BaseModel):
    status: HealthStatus
    cpu_load_avg: float
    memory_usage_mb: int
    thermal_zone0: float

class CIStatus(BaseModel):
    status: HealthStatus
    last_build_hash: str
    tests_passing: bool

class HiveLog(BaseModel):
    status: HealthStatus
    stream_size_kb: int
    active_streams: List[str]

class InfrastructureHealth(BaseModel):
    swarmos: SwarmProcess
    vitals: Vitals
    chimeraci: CIStatus
    hivelog: HiveLog

class Node(BaseModel):
    id: str
    role: Role
    status: HealthStatus
    trust_score: float
    latency_ms: int
    capabilities: List[str]

class SwarmTopology(BaseModel):
    formation: SwarmFormation
    consensus_algorithm: ConsensusAlgorithm
    total_nodes: int
    nodes: List[Node]

class ReasoningTrace(BaseModel):
    trigger: str
    steps: List[str]

class MotorPrimitive(BaseModel):
    profile: str
    torque_limit_nm: float

class CognitiveState(BaseModel):
    cortex_backend: str
    current_intent: str
    reasoning_trace: ReasoningTrace
    motor_primitive: MotorPrimitive

class Hazard(BaseModel):
    type: str
    coordinates: List[float]
    confidence: float
    timestamp_detected: datetime

class EnvironmentContext(BaseModel):
    simulated_weather: str
    friction_coefficient: float
    visibility: str
    network_condition: str
    hazards_detected: List[Hazard]

class ActiveMission(BaseModel):
    id: str
    name: str
    priority: int
    directives: List[str]

class MetahumanOSState(BaseModel):
    """
    The Universal Standard Definition for the Metahuman OS.
    This schema defines the exact structure expected for any compliant system.
    """
    system_identity: SystemIdentity
    infrastructure_health: InfrastructureHealth
    swarm_topology: SwarmTopology
    cognitive_state: CognitiveState
    environment_context: EnvironmentContext
    active_mission: ActiveMission
