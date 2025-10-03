"""
Core domain models for B2B Customer Migration Platform
"""
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ChannelType(str, Enum):
    """Types of integration channels"""
    EDI = "edi"
    SFTP = "sftp"
    REST_API = "rest_api"
    SOAP_API = "soap_api"
    THICK_CLIENT = "thick_client"
    WEB_PORTAL = "web_portal"


class IntegrationChannel(BaseModel):
    """Represents an integration channel for a customer"""
    channel_id: str = Field(..., description="Unique channel identifier")
    channel_type: ChannelType = Field(..., description="Type of integration channel")
    name: str = Field(..., description="Human-readable channel name")
    config: Dict[str, Any] = Field(default_factory=dict, description="Channel configuration")
    legacy_endpoint: Optional[str] = Field(None, description="Legacy system endpoint")
    target_endpoint: Optional[str] = Field(None, description="Modern platform endpoint")
    is_active: bool = Field(default=True, description="Whether channel is currently active")
    transaction_volume: int = Field(default=0, description="Average daily transaction volume")
    
    class Config:
        use_enum_values = True


class Customer(BaseModel):
    """Represents a B2B customer"""
    customer_id: str = Field(..., description="Unique customer identifier")
    name: str = Field(..., description="Customer name")
    industry: Optional[str] = Field(None, description="Customer industry")
    channels: List[IntegrationChannel] = Field(default_factory=list, description="Integration channels")
    business_criticality: str = Field(default="medium", description="Business criticality: low, medium, high, critical")
    compliance_requirements: List[str] = Field(default_factory=list, description="Compliance requirements (e.g., HIPAA, PCI-DSS)")
    contact_email: Optional[str] = Field(None, description="Primary contact email")
    contact_phone: Optional[str] = Field(None, description="Primary contact phone")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


class MigrationStatus(str, Enum):
    """Migration status enum"""
    PENDING = "pending"
    PLANNING = "planning"
    RISK_ASSESSMENT = "risk_assessment"
    SIMULATION = "simulation"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class ChannelMigration(BaseModel):
    """Represents migration of a single channel"""
    channel_id: str
    channel_type: ChannelType
    status: MigrationStatus = MigrationStatus.PENDING
    risk_score: float = Field(0.0, ge=0.0, le=100.0, description="Risk score 0-100")
    playbook_id: Optional[str] = None
    simulation_passed: bool = False
    cutover_timestamp: Optional[datetime] = None
    rollback_available: bool = True
    notes: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class MigrationPlan(BaseModel):
    """Comprehensive migration plan for a customer"""
    plan_id: str = Field(..., description="Unique plan identifier")
    customer_id: str = Field(..., description="Customer being migrated")
    customer_name: str = Field(..., description="Customer name")
    overall_status: MigrationStatus = MigrationStatus.PENDING
    channel_migrations: List[ChannelMigration] = Field(default_factory=list)
    overall_risk_score: float = Field(0.0, ge=0.0, le=100.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    planned_start: Optional[datetime] = None
    planned_completion: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_completion: Optional[datetime] = None
    migration_strategy: str = Field(default="phased", description="Migration strategy: phased, big-bang, parallel")
    
    class Config:
        use_enum_values = True
