"""
Tests for channel-specific playbooks
"""
import pytest

from src.models.customer import IntegrationChannel, ChannelType
from src.channels.playbooks import (
    PlaybookFactory,
    EDIMigrationPlaybook,
    SFTPMigrationPlaybook,
    APIRigrationPlaybook,
    ThickClientMigrationPlaybook
)


def test_playbook_factory_edi():
    """Test creating EDI playbook"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Channel"
    )
    
    playbook = PlaybookFactory.create_playbook(channel)
    assert isinstance(playbook, EDIMigrationPlaybook)


def test_playbook_factory_sftp():
    """Test creating SFTP playbook"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.SFTP,
        name="SFTP Channel"
    )
    
    playbook = PlaybookFactory.create_playbook(channel)
    assert isinstance(playbook, SFTPMigrationPlaybook)


def test_playbook_factory_api():
    """Test creating API playbook"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.REST_API,
        name="API Channel"
    )
    
    playbook = PlaybookFactory.create_playbook(channel)
    assert isinstance(playbook, APIRigrationPlaybook)


def test_edi_playbook_steps():
    """Test EDI playbook generates steps"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Channel",
        config={"protocol": "X12", "version": "4010"}
    )
    
    playbook = EDIMigrationPlaybook(channel)
    steps = playbook.generate_steps()
    
    assert len(steps) > 0
    assert all("step_id" in step for step in steps)
    assert all("name" in step for step in steps)
    assert all("estimated_duration_hours" in step for step in steps)


def test_edi_playbook_prerequisites():
    """Test EDI playbook prerequisites"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Channel"
    )
    
    playbook = EDIMigrationPlaybook(channel)
    prerequisites = playbook.get_prerequisites()
    
    assert len(prerequisites) > 0
    assert any("EDI" in prereq for prereq in prerequisites)


def test_edi_playbook_validation_checklist():
    """Test EDI playbook validation checklist"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Channel"
    )
    
    playbook = EDIMigrationPlaybook(channel)
    checklist = playbook.get_validation_checklist()
    
    assert len(checklist) > 0


def test_edi_playbook_rollback_plan():
    """Test EDI playbook rollback plan"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Channel"
    )
    
    playbook = EDIMigrationPlaybook(channel)
    rollback = playbook.get_rollback_plan()
    
    assert len(rollback) > 0


def test_sftp_playbook_steps():
    """Test SFTP playbook generates steps"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.SFTP,
        name="SFTP Channel"
    )
    
    playbook = SFTPMigrationPlaybook(channel)
    steps = playbook.generate_steps()
    
    assert len(steps) > 0
    assert any("SFTP" in step["name"] for step in steps)


def test_api_playbook_steps():
    """Test API playbook generates steps"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.REST_API,
        name="API Channel",
        config={"api_type": "REST"}
    )
    
    playbook = APIRigrationPlaybook(channel)
    steps = playbook.generate_steps()
    
    assert len(steps) > 0
    assert any("API" in step["name"] for step in steps)


def test_thick_client_playbook_steps():
    """Test thick client playbook generates steps"""
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.THICK_CLIENT,
        name="Desktop App"
    )
    
    playbook = ThickClientMigrationPlaybook(channel)
    steps = playbook.generate_steps()
    
    assert len(steps) > 0
    # Thick client migration should include UAT and training
    step_names = [step["name"] for step in steps]
    assert any("Testing" in name for name in step_names)
    assert any("Training" in name for name in step_names)
