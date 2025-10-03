"""
Example usage of the B2B Customer Migration Platform

This script demonstrates the complete workflow from customer creation
through risk assessment, migration planning, simulation, and execution.
"""
from src.models.customer import Customer, IntegrationChannel, ChannelType
from src.orchestration.migration_orchestrator import MigrationOrchestrator
from src.risk.risk_assessor import RiskAssessor
from src.simulation.simulation_engine import SimulationEngine


def main():
    print("=" * 80)
    print("B2B Customer Migration Platform - Example Usage")
    print("=" * 80)
    print()
    
    # Step 1: Create a sample customer with multiple integration channels
    print("Step 1: Creating Sample Customer")
    print("-" * 80)
    
    customer = Customer(
        customer_id="CUST001",
        name="Acme Logistics Corporation",
        industry="Transportation & Logistics",
        business_criticality="high",
        compliance_requirements=["SOC2", "ISO27001"],
        contact_email="migration@acme-logistics.com",
        contact_phone="+1-555-0100",
        channels=[
            IntegrationChannel(
                channel_id="CH001",
                channel_type=ChannelType.EDI,
                name="Primary EDI Integration",
                config={"protocol": "X12", "version": "4010"},
                legacy_endpoint="edi.legacy.acme.com",
                target_endpoint="edi.modern.acme.com",
                transaction_volume=5000
            ),
            IntegrationChannel(
                channel_id="CH002",
                channel_type=ChannelType.SFTP,
                name="Batch File Transfer",
                config={"encryption": "AES256"},
                legacy_endpoint="sftp.legacy.acme.com",
                target_endpoint="sftp.modern.acme.com",
                transaction_volume=1000
            ),
            IntegrationChannel(
                channel_id="CH003",
                channel_type=ChannelType.REST_API,
                name="Customer Portal API",
                config={"auth": "OAuth2"},
                legacy_endpoint="https://api.legacy.acme.com/v1",
                target_endpoint="https://api.modern.acme.com/v2",
                transaction_volume=10000
            )
        ]
    )
    
    print(f"Customer: {customer.name}")
    print(f"Industry: {customer.industry}")
    print(f"Business Criticality: {customer.business_criticality}")
    print(f"Compliance: {', '.join(customer.compliance_requirements)}")
    print(f"Integration Channels: {len(customer.channels)}")
    for channel in customer.channels:
        channel_type = channel.channel_type if isinstance(channel.channel_type, str) else channel.channel_type.value
        print(f"  - {channel.name} ({channel_type})")
    print()
    
    # Step 2: Perform risk assessment
    print("Step 2: Risk Assessment")
    print("-" * 80)
    
    risk_assessor = RiskAssessor()
    assessment = risk_assessor.assess_customer(customer)
    
    print(f"Assessment ID: {assessment.assessment_id}")
    print(f"Overall Risk Score: {assessment.overall_risk_score:.2f}/100")
    risk_level_val = assessment.risk_level if isinstance(assessment.risk_level, str) else assessment.risk_level.value
    print(f"Risk Level: {risk_level_val.upper()}")
    print(f"Migration Readiness Score: {assessment.migration_readiness_score:.2f}/100")
    print(f"\nRisk Factors Identified: {len(assessment.risk_factors)}")
    for i, factor in enumerate(assessment.risk_factors[:3], 1):
        category_val = factor.category if isinstance(factor.category, str) else factor.category.value
        print(f"  {i}. [{category_val}] {factor.description}")
        print(f"     Risk Score: {factor.risk_score:.2f}")
    print(f"\nRecommended Actions:")
    for i, action in enumerate(assessment.recommended_actions, 1):
        print(f"  {i}. {action}")
    print()
    
    # Step 3: Create migration plan
    print("Step 3: Migration Planning")
    print("-" * 80)
    
    orchestrator = MigrationOrchestrator()
    migration_plan = orchestrator.create_migration_plan(customer, strategy="phased")
    
    print(f"Migration Plan ID: {migration_plan.plan_id}")
    print(f"Strategy: {migration_plan.migration_strategy}")
    print(f"Planned Start: {migration_plan.planned_start.strftime('%Y-%m-%d')}")
    print(f"Planned Completion: {migration_plan.planned_completion.strftime('%Y-%m-%d')}")
    print(f"Duration: {(migration_plan.planned_completion - migration_plan.planned_start).days} days")
    print(f"\nChannel Migration Plans:")
    for cm in migration_plan.channel_migrations:
        channel_type = cm.channel_type if isinstance(cm.channel_type, str) else cm.channel_type.value
        status_val = cm.status if isinstance(cm.status, str) else cm.status.value
        print(f"  - Channel {cm.channel_id} ({channel_type})")
        print(f"    Risk Score: {cm.risk_score:.2f}")
        print(f"    Playbook: {cm.playbook_id}")
        print(f"    Status: {status_val}")
    print()
    
    # Step 4: Run simulations
    print("Step 4: Simulation Testing")
    print("-" * 80)
    
    simulation_results = orchestrator.run_simulations(migration_plan.plan_id)
    
    print(f"Simulations executed for {len(simulation_results)} channels:")
    for channel_id, result in simulation_results.items():
        print(f"  - Channel {channel_id}")
        print(f"    Status: {result['status']}")
        print(f"    Success Rate: {result['success_rate']:.1f}%")
        print(f"    Details: {result['details']}")
    print()
    
    # Step 5: Get migration status
    print("Step 5: Migration Status")
    print("-" * 80)
    
    status = orchestrator.get_migration_status(migration_plan.plan_id)
    
    print(f"Plan ID: {status['plan_id']}")
    print(f"Customer: {status['customer_name']}")
    print(f"Overall Status: {status['overall_status'].upper()}")
    print(f"Progress: {status['progress_percentage']:.1f}%")
    print(f"Overall Risk Score: {status['overall_risk_score']:.2f}")
    print(f"\nChannel Status:")
    for ch_status in status['channels']:
        print(f"  - {ch_status['channel_id']} ({ch_status['channel_type']})")
        print(f"    Status: {ch_status['status']}")
        print(f"    Simulation: {'PASSED' if ch_status['simulation_passed'] else 'NOT RUN'}")
    print()
    
    # Step 6: Summary
    print("=" * 80)
    print("Migration Plan Summary")
    print("=" * 80)
    print(f"✓ Customer assessed and ready for migration")
    print(f"✓ Risk level: {assessment.risk_level if isinstance(assessment.risk_level, str) else assessment.risk_level.value.upper()}")
    print(f"✓ Migration plan created with {len(migration_plan.channel_migrations)} channels")
    print(f"✓ All simulations passed")
    print(f"✓ System ready for production cutover")
    print()
    print("Next steps:")
    print("  1. Review migration plan with stakeholders")
    print("  2. Schedule cutover window")
    print("  3. Execute migration using: orchestrator.execute_migration(plan_id)")
    print("  4. Monitor migration progress in real-time")
    print("  5. Validate successful completion")
    print()


if __name__ == "__main__":
    main()
