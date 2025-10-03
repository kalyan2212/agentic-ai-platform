"""
Tests for risk assessment module
"""
import pytest

from src.models.customer import Customer, IntegrationChannel, ChannelType
from src.risk.risk_assessor import RiskAssessor
from src.models.risk import RiskCategory, RiskSeverity


def test_risk_assessor_initialization():
    """Test risk assessor initialization"""
    assessor = RiskAssessor()
    assert assessor is not None
    assert len(assessor.risk_weights) == 5


def test_assess_low_criticality_customer():
    """Test assessing a low criticality customer"""
    customer = Customer(
        customer_id="CUST001",
        name="Low Risk Corp",
        business_criticality="low",
        channels=[
            IntegrationChannel(
                channel_id="CH001",
                channel_type=ChannelType.REST_API,
                name="Simple API"
            )
        ]
    )
    
    assessor = RiskAssessor()
    assessment = assessor.assess_customer(customer)
    
    assert assessment.customer_id == "CUST001"
    assert assessment.overall_risk_score < 50.0
    assert assessment.migration_readiness_score > 50.0
    assert len(assessment.recommended_actions) > 0


def test_assess_high_criticality_customer():
    """Test assessing a high criticality customer"""
    customer = Customer(
        customer_id="CUST002",
        name="High Risk Corp",
        business_criticality="critical",
        compliance_requirements=["HIPAA", "PCI-DSS"],
        channels=[
            IntegrationChannel(
                channel_id="CH001",
                channel_type=ChannelType.EDI,
                name="EDI Integration"
            ),
            IntegrationChannel(
                channel_id="CH002",
                channel_type=ChannelType.EDI,
                name="EDI Integration 2"
            ),
            IntegrationChannel(
                channel_id="CH003",
                channel_type=ChannelType.THICK_CLIENT,
                name="Desktop App"
            ),
            IntegrationChannel(
                channel_id="CH004",
                channel_type=ChannelType.THICK_CLIENT,
                name="Desktop App 2"
            ),
            IntegrationChannel(
                channel_id="CH005",
                channel_type=ChannelType.THICK_CLIENT,
                name="Desktop App 3"
            ),
            IntegrationChannel(
                channel_id="CH006",
                channel_type=ChannelType.THICK_CLIENT,
                name="Desktop App 4"
            )
        ]
    )
    
    assessor = RiskAssessor()
    assessment = assessor.assess_customer(customer)
    
    assert assessment.customer_id == "CUST002"
    # With critical business level, compliance requirements, and many legacy channels,
    # risk score should be elevated
    assert assessment.overall_risk_score > 35.0
    assert assessment.risk_level in [RiskSeverity.MEDIUM, RiskSeverity.HIGH, RiskSeverity.CRITICAL]
    assert len(assessment.risk_factors) > 0


def test_assess_channel_risk():
    """Test channel-specific risk assessment"""
    customer = Customer(
        customer_id="CUST001",
        name="Test Corp"
    )
    
    channel = IntegrationChannel(
        channel_id="CH001",
        channel_type=ChannelType.EDI,
        name="EDI Channel",
        transaction_volume=15000
    )
    
    assessor = RiskAssessor()
    assessment = assessor.assess_channel(customer, channel)
    
    assert assessment.channel_id == "CH001"
    assert len(assessment.risk_factors) > 0
    # High transaction volume should contribute to risk
    assert assessment.overall_risk_score > 0


def test_compliance_risk_assessment():
    """Test compliance requirements increase risk"""
    customer_without_compliance = Customer(
        customer_id="CUST001",
        name="No Compliance Corp",
        business_criticality="medium"
    )
    
    customer_with_compliance = Customer(
        customer_id="CUST002",
        name="Compliance Corp",
        business_criticality="medium",
        compliance_requirements=["HIPAA", "SOC2"]
    )
    
    assessor = RiskAssessor()
    assessment1 = assessor.assess_customer(customer_without_compliance)
    assessment2 = assessor.assess_customer(customer_with_compliance)
    
    # Customer with compliance requirements should have higher risk
    assert assessment2.overall_risk_score > assessment1.overall_risk_score
