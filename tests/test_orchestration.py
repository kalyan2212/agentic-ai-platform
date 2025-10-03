"""
Tests for migration orchestrator
"""
import pytest

from src.models.customer import Customer, IntegrationChannel, ChannelType, MigrationStatus
from src.orchestration.migration_orchestrator import MigrationOrchestrator


def test_orchestrator_initialization():
    """Test orchestrator initialization"""
    orchestrator = MigrationOrchestrator()
    assert orchestrator is not None
    assert orchestrator.risk_assessor is not None
    assert orchestrator.simulation_engine is not None


def test_create_migration_plan():
    """Test creating a migration plan"""
    customer = Customer(
        customer_id="CUST001",
        name="Test Corp",
        channels=[
            IntegrationChannel(
                channel_id="CH001",
                channel_type=ChannelType.REST_API,
                name="API Integration"
            ),
            IntegrationChannel(
                channel_id="CH002",
                channel_type=ChannelType.SFTP,
                name="SFTP Integration"
            )
        ]
    )
    
    orchestrator = MigrationOrchestrator()
    plan = orchestrator.create_migration_plan(customer, strategy="phased")
    
    assert plan.customer_id == "CUST001"
    assert plan.migration_strategy == "phased"
    assert len(plan.channel_migrations) == 2
    assert plan.overall_status == MigrationStatus.PLANNING
    assert plan.planned_start is not None
    assert plan.planned_completion is not None


def test_migration_plan_channel_assessment():
    """Test that migration plan includes channel assessments"""
    customer = Customer(
        customer_id="CUST001",
        name="Test Corp",
        channels=[
            IntegrationChannel(
                channel_id="CH001",
                channel_type=ChannelType.EDI,
                name="EDI Integration"
            )
        ]
    )
    
    orchestrator = MigrationOrchestrator()
    plan = orchestrator.create_migration_plan(customer)
    
    assert len(plan.channel_migrations) == 1
    channel_migration = plan.channel_migrations[0]
    assert channel_migration.channel_id == "CH001"
    assert channel_migration.channel_type == ChannelType.EDI
    assert channel_migration.risk_score >= 0.0
    assert len(channel_migration.notes) > 0


def test_get_migration_status():
    """Test getting migration status"""
    customer = Customer(
        customer_id="CUST001",
        name="Test Corp",
        channels=[
            IntegrationChannel(
                channel_id="CH001",
                channel_type=ChannelType.REST_API,
                name="API"
            )
        ]
    )
    
    orchestrator = MigrationOrchestrator()
    plan = orchestrator.create_migration_plan(customer)
    
    status = orchestrator.get_migration_status(plan.plan_id)
    
    assert status["plan_id"] == plan.plan_id
    assert status["customer_id"] == "CUST001"
    assert status["overall_status"] == MigrationStatus.PLANNING.value
    assert "channels" in status
    assert len(status["channels"]) == 1


def test_migration_plan_not_found():
    """Test error handling for non-existent plan"""
    orchestrator = MigrationOrchestrator()
    
    with pytest.raises(ValueError, match="not found"):
        orchestrator.get_migration_status("INVALID_PLAN_ID")


def test_phased_vs_bigbang_strategy():
    """Test different migration strategies"""
    customer = Customer(
        customer_id="CUST001",
        name="Test Corp",
        channels=[
            IntegrationChannel(
                channel_id=f"CH{i:03d}",
                channel_type=ChannelType.REST_API,
                name=f"API {i}"
            )
            for i in range(5)
        ]
    )
    
    orchestrator = MigrationOrchestrator()
    
    phased_plan = orchestrator.create_migration_plan(customer, strategy="phased")
    bigbang_plan = orchestrator.create_migration_plan(customer, strategy="big-bang")
    
    # Phased should take longer than big-bang
    phased_duration = (phased_plan.planned_completion - phased_plan.planned_start).days
    bigbang_duration = (bigbang_plan.planned_completion - bigbang_plan.planned_start).days
    
    assert phased_duration > bigbang_duration
