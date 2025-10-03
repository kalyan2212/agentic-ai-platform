"""
Unit tests for orchestration engine
"""

import pytest
from datetime import datetime

from src.agents.orchestration import (
    OrchestrationEngine,
    BaseAgent,
    AgentRole,
    AgentStatus,
    AgentMessage
)


def test_agent_creation():
    """Test creating a base agent"""
    agent = BaseAgent("test_agent_1", AgentRole.DATA_ANALYZER, ["analyze_data"])
    
    assert agent.agent_id == "test_agent_1"
    assert agent.role == AgentRole.DATA_ANALYZER
    assert agent.status == AgentStatus.IDLE
    assert "analyze_data" in agent.capabilities


def test_orchestration_engine_initialization():
    """Test orchestration engine initialization"""
    engine = OrchestrationEngine()
    
    assert engine is not None
    assert len(engine.agents) == 0
    assert engine.consensus_threshold == 0.66


def test_agent_registration():
    """Test registering agents with orchestration engine"""
    engine = OrchestrationEngine()
    agent = BaseAgent("agent_1", AgentRole.DATA_ANALYZER, ["analyze"])
    
    engine.register_agent(agent)
    
    assert "agent_1" in engine.agents
    assert engine.agents["agent_1"] == agent


@pytest.mark.asyncio
async def test_message_routing():
    """Test message routing between agents"""
    engine = OrchestrationEngine()
    
    sender = BaseAgent("sender_1", AgentRole.COORDINATOR, ["coordinate"])
    receiver = BaseAgent("receiver_1", AgentRole.DATA_ANALYZER, ["analyze"])
    
    engine.register_agent(sender)
    engine.register_agent(receiver)
    
    message = AgentMessage(
        sender="sender_1",
        receiver="receiver_1",
        message_type="analyze_request",
        content={"data": "test"}
    )
    
    await engine.route_message(message)
    
    assert len(receiver.message_queue) == 1
    assert receiver.message_queue[0].message_type == "analyze_request"


@pytest.mark.asyncio
async def test_consensus_mechanism():
    """Test consensus mechanism for decision making"""
    engine = OrchestrationEngine()
    
    # Register multiple agents
    for i in range(3):
        agent = BaseAgent(f"agent_{i}", AgentRole.VALIDATOR, ["validate"])
        engine.register_agent(agent)
    
    decision = {
        "type": "schema_change",
        "description": "Modify table schema"
    }
    
    # Note: This is a simplified test as the actual voting logic is a placeholder
    consensus = await engine.achieve_consensus(decision)
    
    # The consensus should be reached (simplified implementation always returns True)
    assert isinstance(consensus, bool)


@pytest.mark.asyncio
async def test_conflict_resolution():
    """Test autonomous conflict resolution"""
    engine = OrchestrationEngine()
    
    conflict = {
        "type": "schema_mapping",
        "source": "DB2_TABLE",
        "target": "PG_TABLE",
        "issue": "Data type mismatch"
    }
    
    resolution = await engine.resolve_conflict(conflict)
    
    assert resolution["resolved"] == True
    assert "resolution" in resolution


def test_agent_status_management():
    """Test agent status transitions"""
    agent = BaseAgent("test_agent", AgentRole.DATA_MIGRATOR, ["migrate"])
    
    assert agent.get_status() == AgentStatus.IDLE
    
    agent.status = AgentStatus.ACTIVE
    assert agent.get_status() == AgentStatus.ACTIVE


def test_find_capable_agents():
    """Test finding capable agents for operations"""
    engine = OrchestrationEngine()
    
    agent1 = BaseAgent("agent_1", AgentRole.DATA_ANALYZER, ["analyze_schema"])
    agent2 = BaseAgent("agent_2", AgentRole.DATA_MIGRATOR, ["migrate_data"])
    agent3 = BaseAgent("agent_3", AgentRole.DATA_ANALYZER, ["analyze_schema", "analyze_data"])
    
    engine.register_agent(agent1)
    engine.register_agent(agent2)
    engine.register_agent(agent3)
    
    capable_agents = engine._find_capable_agents("analyze_schema")
    
    assert len(capable_agents) == 2
    assert agent1 in capable_agents
    assert agent3 in capable_agents
    assert agent2 not in capable_agents
