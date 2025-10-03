"""
Risk Assessment Engine
Automated risk analysis and migration readiness scoring
"""
from typing import List, Dict
import uuid
from datetime import datetime

from src.models.customer import Customer, IntegrationChannel, ChannelType
from src.models.risk import (
    RiskAssessment,
    RiskFactor,
    RiskCategory,
    RiskSeverity,
    MitigationAction
)


class RiskAssessor:
    """
    Patent-worthy innovation: Automated risk analysis and migration readiness scoring
    
    This class implements intelligent risk assessment for B2B customer migrations,
    analyzing technical, business, compliance, and operational factors.
    """
    
    def __init__(self):
        self.risk_weights = {
            RiskCategory.TECHNICAL: 0.25,
            RiskCategory.BUSINESS: 0.30,
            RiskCategory.COMPLIANCE: 0.25,
            RiskCategory.OPERATIONAL: 0.15,
            RiskCategory.INTEGRATION: 0.05
        }
    
    def assess_customer(self, customer: Customer) -> RiskAssessment:
        """
        Perform comprehensive risk assessment for a customer
        
        Args:
            customer: Customer to assess
            
        Returns:
            RiskAssessment with detailed risk factors and scores
        """
        assessment_id = f"RISK-{uuid.uuid4().hex[:8]}"
        risk_factors = []
        
        # Assess business criticality
        risk_factors.extend(self._assess_business_criticality(customer))
        
        # Assess compliance requirements
        risk_factors.extend(self._assess_compliance(customer))
        
        # Assess channel complexity
        risk_factors.extend(self._assess_channel_complexity(customer))
        
        # Assess operational factors
        risk_factors.extend(self._assess_operational_factors(customer))
        
        # Calculate overall risk score
        overall_risk_score = self._calculate_overall_risk(risk_factors)
        risk_level = self._determine_risk_level(overall_risk_score)
        
        # Calculate migration readiness score (inverse of risk)
        readiness_score = 100.0 - overall_risk_score
        
        # Generate recommended actions
        recommended_actions = self._generate_recommendations(risk_factors, customer)
        
        return RiskAssessment(
            assessment_id=assessment_id,
            customer_id=customer.customer_id,
            risk_factors=risk_factors,
            overall_risk_score=overall_risk_score,
            risk_level=risk_level,
            migration_readiness_score=readiness_score,
            recommended_actions=recommended_actions,
            assessed_at=datetime.utcnow()
        )
    
    def assess_channel(self, customer: Customer, channel: IntegrationChannel) -> RiskAssessment:
        """
        Assess risk for a specific channel
        
        Args:
            customer: Customer owning the channel
            channel: Integration channel to assess
            
        Returns:
            RiskAssessment for the specific channel
        """
        assessment_id = f"RISK-CH-{uuid.uuid4().hex[:8]}"
        risk_factors = []
        
        # Channel-specific technical risks
        risk_factors.extend(self._assess_channel_technical_risk(channel))
        
        # Integration complexity
        risk_factors.extend(self._assess_integration_complexity(channel))
        
        # Transaction volume risk
        risk_factors.extend(self._assess_transaction_volume_risk(channel))
        
        overall_risk_score = self._calculate_overall_risk(risk_factors)
        risk_level = self._determine_risk_level(overall_risk_score)
        readiness_score = 100.0 - overall_risk_score
        
        recommended_actions = self._generate_channel_recommendations(risk_factors, channel)
        
        return RiskAssessment(
            assessment_id=assessment_id,
            customer_id=customer.customer_id,
            channel_id=channel.channel_id,
            risk_factors=risk_factors,
            overall_risk_score=overall_risk_score,
            risk_level=risk_level,
            migration_readiness_score=readiness_score,
            recommended_actions=recommended_actions,
            assessed_at=datetime.utcnow()
        )
    
    def _assess_business_criticality(self, customer: Customer) -> List[RiskFactor]:
        """Assess business criticality risks"""
        factors = []
        
        criticality_map = {
            "low": (10.0, 30.0),
            "medium": (30.0, 50.0),
            "high": (60.0, 80.0),
            "critical": (80.0, 95.0)
        }
        
        impact, likelihood = criticality_map.get(customer.business_criticality.lower(), (30.0, 50.0))
        
        factors.append(RiskFactor(
            factor_id=f"BIZ-CRIT-{uuid.uuid4().hex[:6]}",
            category=RiskCategory.BUSINESS,
            severity=self._score_to_severity((impact * likelihood) / 100.0),
            description=f"Business criticality level: {customer.business_criticality}",
            impact_score=impact,
            likelihood_score=likelihood,
            mitigation_strategy="Implement parallel run and staged rollout for critical customers"
        ))
        
        return factors
    
    def _assess_compliance(self, customer: Customer) -> List[RiskFactor]:
        """Assess compliance-related risks"""
        factors = []
        
        if customer.compliance_requirements:
            for requirement in customer.compliance_requirements:
                impact = 70.0  # Compliance failures have high impact
                likelihood = 40.0  # Moderate likelihood if not properly managed
                
                factors.append(RiskFactor(
                    factor_id=f"COMP-{uuid.uuid4().hex[:6]}",
                    category=RiskCategory.COMPLIANCE,
                    severity=RiskSeverity.HIGH,
                    description=f"Compliance requirement: {requirement}",
                    impact_score=impact,
                    likelihood_score=likelihood,
                    mitigation_strategy=f"Ensure {requirement} compliance validation in simulation phase"
                ))
        
        return factors
    
    def _assess_channel_complexity(self, customer: Customer) -> List[RiskFactor]:
        """Assess risk based on number and types of channels"""
        factors = []
        
        num_channels = len(customer.channels)
        
        if num_channels > 5:
            factors.append(RiskFactor(
                factor_id=f"CH-COUNT-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.INTEGRATION,
                severity=RiskSeverity.HIGH,
                description=f"High number of integration channels: {num_channels}",
                impact_score=65.0,
                likelihood_score=60.0,
                mitigation_strategy="Prioritize channels and migrate in phases"
            ))
        
        # Check for legacy channel types
        legacy_types = [ChannelType.EDI, ChannelType.THICK_CLIENT]
        has_legacy = any(ch.channel_type in legacy_types for ch in customer.channels)
        
        if has_legacy:
            factors.append(RiskFactor(
                factor_id=f"LEGACY-CH-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.TECHNICAL,
                severity=RiskSeverity.MEDIUM,
                description="Customer uses legacy channel types (EDI or thick client)",
                impact_score=55.0,
                likelihood_score=50.0,
                mitigation_strategy="Use channel-specific migration playbooks for legacy integrations"
            ))
        
        return factors
    
    def _assess_operational_factors(self, customer: Customer) -> List[RiskFactor]:
        """Assess operational risks"""
        factors = []
        
        # Check if contact information is available
        if not customer.contact_email and not customer.contact_phone:
            factors.append(RiskFactor(
                factor_id=f"OP-CONTACT-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.OPERATIONAL,
                severity=RiskSeverity.MEDIUM,
                description="No contact information available for customer",
                impact_score=40.0,
                likelihood_score=60.0,
                mitigation_strategy="Establish communication channel before migration"
            ))
        
        return factors
    
    def _assess_channel_technical_risk(self, channel: IntegrationChannel) -> List[RiskFactor]:
        """Assess technical risks for a channel"""
        factors = []
        
        # Channel type complexity
        complexity_map = {
            ChannelType.EDI: (70.0, "EDI migrations require protocol mapping and validation"),
            ChannelType.THICK_CLIENT: (65.0, "Thick client requires application deployment and testing"),
            ChannelType.SFTP: (40.0, "SFTP migration requires file format validation"),
            ChannelType.SOAP_API: (50.0, "SOAP API migration requires interface compatibility"),
            ChannelType.REST_API: (30.0, "REST API migration is relatively straightforward"),
            ChannelType.WEB_PORTAL: (35.0, "Web portal migration requires UI/UX validation")
        }
        
        impact, description = complexity_map.get(channel.channel_type, (40.0, "Standard channel migration"))
        
        factors.append(RiskFactor(
            factor_id=f"TECH-{uuid.uuid4().hex[:6]}",
            category=RiskCategory.TECHNICAL,
            severity=self._score_to_severity(impact),
            description=description,
            impact_score=impact,
            likelihood_score=50.0,
            mitigation_strategy="Use channel-specific playbook and thorough testing"
        ))
        
        return factors
    
    def _assess_integration_complexity(self, channel: IntegrationChannel) -> List[RiskFactor]:
        """Assess integration complexity"""
        factors = []
        
        # Check if endpoints are configured
        if not channel.target_endpoint:
            factors.append(RiskFactor(
                factor_id=f"INT-ENDPOINT-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.INTEGRATION,
                severity=RiskSeverity.HIGH,
                description="Target endpoint not configured",
                impact_score=75.0,
                likelihood_score=100.0,
                mitigation_strategy="Configure and validate target endpoint before migration"
            ))
        
        return factors
    
    def _assess_transaction_volume_risk(self, channel: IntegrationChannel) -> List[RiskFactor]:
        """Assess risk based on transaction volume"""
        factors = []
        
        if channel.transaction_volume > 10000:
            factors.append(RiskFactor(
                factor_id=f"VOL-HIGH-{uuid.uuid4().hex[:6]}",
                category=RiskCategory.OPERATIONAL,
                severity=RiskSeverity.HIGH,
                description=f"High transaction volume: {channel.transaction_volume}/day",
                impact_score=70.0,
                likelihood_score=45.0,
                mitigation_strategy="Implement load testing and performance validation"
            ))
        
        return factors
    
    def _calculate_overall_risk(self, risk_factors: List[RiskFactor]) -> float:
        """Calculate weighted overall risk score"""
        if not risk_factors:
            return 0.0
        
        category_scores = {cat: [] for cat in RiskCategory}
        
        for factor in risk_factors:
            category_scores[factor.category].append(factor.risk_score)
        
        weighted_score = 0.0
        for category, scores in category_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                weighted_score += avg_score * self.risk_weights.get(category, 0.1)
        
        return min(100.0, weighted_score)
    
    def _determine_risk_level(self, risk_score: float) -> RiskSeverity:
        """Determine risk level from score"""
        if risk_score >= 70.0:
            return RiskSeverity.CRITICAL
        elif risk_score >= 50.0:
            return RiskSeverity.HIGH
        elif risk_score >= 30.0:
            return RiskSeverity.MEDIUM
        else:
            return RiskSeverity.LOW
    
    def _score_to_severity(self, score: float) -> RiskSeverity:
        """Convert numeric score to severity"""
        return self._determine_risk_level(score)
    
    def _generate_recommendations(self, risk_factors: List[RiskFactor], customer: Customer) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        high_risk_factors = [f for f in risk_factors if f.severity in [RiskSeverity.HIGH, RiskSeverity.CRITICAL]]
        
        if high_risk_factors:
            recommendations.append("Implement phased migration approach due to high-risk factors")
            recommendations.append("Conduct thorough simulation testing before cutover")
        
        if customer.compliance_requirements:
            recommendations.append("Validate compliance requirements in test environment")
        
        if len(customer.channels) > 3:
            recommendations.append("Prioritize channels by business impact and migrate sequentially")
        
        recommendations.append("Establish rollback procedures for each migration phase")
        recommendations.append("Set up real-time monitoring during cutover period")
        
        return recommendations
    
    def _generate_channel_recommendations(self, risk_factors: List[RiskFactor], channel: IntegrationChannel) -> List[str]:
        """Generate channel-specific recommendations"""
        recommendations = []
        
        channel_type_value = channel.channel_type if isinstance(channel.channel_type, str) else channel.channel_type.value
        recommendations.append(f"Use {channel_type_value} migration playbook")
        recommendations.append("Validate channel configuration in simulation environment")
        
        if channel.transaction_volume > 5000:
            recommendations.append("Conduct load testing before production cutover")
        
        recommendations.append("Implement transaction logging for troubleshooting")
        
        return recommendations
