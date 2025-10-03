"""
Tests for simulation engine
"""
import pytest

from src.models.customer import IntegrationChannel, ChannelType
from src.simulation.simulation_engine import SimulationEngine
from src.models.simulation import SimulationStatus


def test_simulation_engine_initialization():
    """Test simulation engine initialization"""
    engine = SimulationEngine()
    assert engine is not None
    assert len(engine.scenario_templates) > 0


def test_create_simulation_edi():
    """Test creating simulation for EDI channel"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Channel"
    )
    
    engine = SimulationEngine()
    simulation = engine.create_simulation("CUST001", channel)
    
    assert simulation.customer_id == "CUST001"
    assert simulation.channel_id == "CH001"
    assert len(simulation.scenarios) > 0
    assert simulation.overall_status == SimulationStatus.PENDING


def test_create_simulation_sftp():
    """Test creating simulation for SFTP channel"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.SFTP,
        name="SFTP Channel"
    )
    
    engine = SimulationEngine()
    simulation = engine.create_simulation("CUST001", channel)
    
    assert len(simulation.scenarios) > 0
    # SFTP should have file upload/download scenarios
    scenario_names = [s.name for s in simulation.scenarios]
    assert any("Upload" in name or "Download" in name for name in scenario_names)


def test_execute_simulation():
    """Test executing a simulation"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.REST_API,
        name="API Channel"
    )
    
    engine = SimulationEngine()
    simulation = engine.create_simulation("CUST001", channel)
    
    # Execute simulation
    result = engine.execute_simulation(simulation)
    
    assert result.overall_status in [SimulationStatus.PASSED, SimulationStatus.FAILED]
    assert len(result.results) == len(result.scenarios)
    assert result.started_at is not None
    assert result.completed_at is not None
    assert result.success_rate >= 0.0
    assert result.success_rate <= 100.0


def test_simulation_scenarios_have_required_fields():
    """Test that scenarios have all required fields"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.REST_API,
        name="API Channel"
    )
    
    engine = SimulationEngine()
    simulation = engine.create_simulation("CUST001", channel)
    
    for scenario in simulation.scenarios:
        assert scenario.scenario_id is not None
        assert scenario.name is not None
        assert scenario.description is not None
        assert scenario.channel_type == ChannelType.REST_API.value
        assert scenario.test_data is not None
        assert scenario.expected_results is not None


def test_simulation_passed_property():
    """Test simulation passed property"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.REST_API,
        name="API Channel"
    )
    
    engine = SimulationEngine()
    simulation = engine.create_simulation("CUST001", channel)
    
    # Before execution
    assert not simulation.passed
    
    # After execution
    result = engine.execute_simulation(simulation)
    # Passed is true if status is PASSED and success_rate >= 95
    if result.overall_status == SimulationStatus.PASSED and result.success_rate >= 95.0:
        assert result.passed
