"""
Simulation and testing models
"""
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SimulationStatus(str, Enum):
    """Simulation execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ABORTED = "aborted"


class TestScenario(BaseModel):
    """Test scenario for migration validation"""
    scenario_id: str
    name: str
    description: str
    channel_type: str
    test_data: Dict[str, Any] = Field(default_factory=dict)
    expected_results: Dict[str, Any] = Field(default_factory=dict)
    validation_rules: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class SimulationResult(BaseModel):
    """Result of a simulation run"""
    result_id: str
    scenario_id: str
    status: SimulationStatus
    success: bool
    execution_time_ms: int
    legacy_output: Optional[Dict[str, Any]] = None
    modern_output: Optional[Dict[str, Any]] = None
    differences: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


class MigrationSimulation(BaseModel):
    """Complete migration simulation"""
    simulation_id: str
    customer_id: str
    channel_id: str
    scenarios: List[TestScenario] = Field(default_factory=list)
    results: List[SimulationResult] = Field(default_factory=list)
    overall_status: SimulationStatus = SimulationStatus.PENDING
    success_rate: float = Field(0.0, ge=0.0, le=100.0)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    @property
    def passed(self) -> bool:
        """Check if simulation passed"""
        return self.overall_status == SimulationStatus.PASSED and self.success_rate >= 95.0
    
    class Config:
        use_enum_values = True
