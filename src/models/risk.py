"""
Risk assessment models for migration planning
"""
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RiskCategory(str, Enum):
    """Categories of migration risks"""
    TECHNICAL = "technical"
    BUSINESS = "business"
    COMPLIANCE = "compliance"
    OPERATIONAL = "operational"
    INTEGRATION = "integration"


class RiskSeverity(str, Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskFactor(BaseModel):
    """Individual risk factor"""
    factor_id: str
    category: RiskCategory
    severity: RiskSeverity
    description: str
    impact_score: float = Field(..., ge=0.0, le=100.0)
    likelihood_score: float = Field(..., ge=0.0, le=100.0)
    mitigation_strategy: Optional[str] = None
    
    @property
    def risk_score(self) -> float:
        """Calculate risk score as impact × likelihood"""
        return (self.impact_score * self.likelihood_score) / 100.0
    
    class Config:
        use_enum_values = True


class RiskAssessment(BaseModel):
    """Complete risk assessment for a customer/channel"""
    assessment_id: str
    customer_id: str
    channel_id: Optional[str] = None
    risk_factors: List[RiskFactor] = Field(default_factory=list)
    overall_risk_score: float = Field(0.0, ge=0.0, le=100.0)
    risk_level: RiskSeverity = RiskSeverity.LOW
    migration_readiness_score: float = Field(0.0, ge=0.0, le=100.0)
    recommended_actions: List[str] = Field(default_factory=list)
    assessed_at: datetime = Field(default_factory=datetime.utcnow)
    assessed_by: str = Field(default="system")
    
    class Config:
        use_enum_values = True


class MitigationAction(BaseModel):
    """Risk mitigation action"""
    action_id: str
    risk_factor_id: str
    action_type: str  # e.g., "backup", "parallel_run", "staged_rollout"
    description: str
    estimated_risk_reduction: float = Field(..., ge=0.0, le=100.0)
    implementation_cost: str  # e.g., "low", "medium", "high"
    required: bool = True
    completed: bool = False
    
    class Config:
        use_enum_values = True
