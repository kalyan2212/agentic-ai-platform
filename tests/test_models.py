"""
Tests for core domain models
"""
import pytest
from datetime import datetime

from src.models.customer import (
    Customer,
    IntegrationChannel,
    ChannelType,
    MigrationPlan,
    ChannelMigration,
    MigrationStatus
)
from src.models.risk import (
    RiskAssessment,
    RiskFactor,
    RiskCategory,
    RiskSeverity
)


def test_create_customer():
    """Test creating a customer"""
    customer = Customer(
        customer_id="CUST001",
        name="Test Corp",
        industry="Technology"
    )
    
    assert customer.customer_id == "CUST001"
    assert customer.name == "Test Corp"
    assert customer.industry == "Technology"
    assert len(customer.channels) == 0


def test_create_integration_channel():
    """Test creating an integration channel"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Integration",
        config={"protocol": "X12", "version": "4010"}
    )
    
    assert channel.channel_id == "CH001"
    assert channel.channel_type == ChannelType.EDI
    assert channel.config["protocol"] == "X12"
    assert channel.is_active is True


def test_customer_with_channels():
    """Test customer with multiple channels"""
    channels = [
        IntegrationChannel(
            channel_id="CH001",
            channel_type=ChannelType.EDI,
            name="EDI Integration"
        ),
        IntegrationChannel(
            channel_id="CH002",
            channel_type=ChannelType.REST_API,
            name="REST API"
        )
    ]
    
    customer = Customer(
        customer_id="CUST001",
        name="Multi-Channel Corp",
        channels=channels
    )
    
    assert len(customer.channels) == 2
    assert customer.channels[0].channel_type == ChannelType.EDI
    assert customer.channels[1].channel_type == ChannelType.REST_API


def test_migration_plan_creation():
    """Test creating a migration plan"""
    plan = MigrationPlan(
        plan_id="PLAN001",
        customer_id="CUST001",
        customer_name="Test Corp",
        overall_status=MigrationStatus.PLANNING
    )
    
    assert plan.plan_id == "PLAN001"
    assert plan.overall_status == MigrationStatus.PLANNING
    assert plan.overall_risk_score == 0.0


def test_risk_factor_score_calculation():
    """Test risk factor score calculation"""
    risk_factor = RiskFactor(
        factor_id="RISK001",
        category=RiskCategory.TECHNICAL,
        severity=RiskSeverity.HIGH,
        description="Test risk",
        impact_score=80.0,
        likelihood_score=50.0
    )
    
    # Risk score should be (80 * 50) / 100 = 40.0
    assert risk_factor.risk_score == 40.0


def test_channel_migration():
    """Test channel migration model"""
    channel_migration = ChannelMigration(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        status=MigrationStatus.PENDING,
        risk_score=45.5
    )
    
    assert channel_migration.status == MigrationStatus.PENDING
    assert channel_migration.risk_score == 45.5
    assert channel_migration.rollback_available is True
