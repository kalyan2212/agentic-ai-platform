"""
Example: Complete End-to-End Migration Simulation

Demonstrates a full migration from DB2/VSAM mainframe to PostgreSQL/microservices.
"""

import asyncio
from datetime import datetime

from src.migration.orchestrator import MigrationOrchestrator
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType, VSAMFile, VSAMFileType
from src.data_generators.synthetic_data import SyntheticDataGenerator


async def run_complete_migration_example():
    """Run a complete end-to-end migration simulation"""
    
    print("=" * 80)
    print("Enterprise Agentic Migration Platform - Complete Migration Example")
    print("=" * 80)
    print()
    
    # Initialize components
    orchestrator = MigrationOrchestrator()
    data_generator = SyntheticDataGenerator(seed=42)
    
    print("Step 1: Setting up legacy mainframe environment...")
    print("-" * 80)
    
    # Create DB2 customer table
    customer_table = DB2Table(
        schema="LEGACY",
        table_name="CUSTOMERS",
        columns=[
            DB2Column("CUSTOMER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("FIRST_NAME", DB2DataType.VARCHAR, length=20),
            DB2Column("LAST_NAME", DB2DataType.VARCHAR, length=30),
            DB2Column("EMAIL", DB2DataType.VARCHAR, length=50),
            DB2Column("PHONE", DB2DataType.VARCHAR, length=15),
            DB2Column("ADDRESS", DB2DataType.VARCHAR, length=60),
            DB2Column("CITY", DB2DataType.VARCHAR, length=30),
            DB2Column("STATE", DB2DataType.CHAR, length=2),
            DB2Column("ZIP_CODE", DB2DataType.VARCHAR, length=10),
            DB2Column("ACCOUNT_BALANCE", DB2DataType.DECIMAL, precision=10, scale=2),
            DB2Column("CREATED_DATE", DB2DataType.DATE),
            DB2Column("STATUS", DB2DataType.VARCHAR, length=20)
        ],
        primary_key=["CUSTOMER_ID"]
    )
    
    # Create DB2 transactions table
    transaction_table = DB2Table(
        schema="LEGACY",
        table_name="TRANSACTIONS",
        columns=[
            DB2Column("TRANSACTION_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("CUSTOMER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("TRANSACTION_TYPE", DB2DataType.VARCHAR, length=20),
            DB2Column("AMOUNT", DB2DataType.DECIMAL, precision=10, scale=2),
            DB2Column("TRANSACTION_DATE", DB2DataType.TIMESTAMP),
            DB2Column("DESCRIPTION", DB2DataType.VARCHAR, length=100),
            DB2Column("STATUS", DB2DataType.VARCHAR, length=20),
            DB2Column("MERCHANT_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("CHANNEL", DB2DataType.VARCHAR, length=20)
        ],
        primary_key=["TRANSACTION_ID"]
    )
    
    # Register tables with legacy environment
    orchestrator.legacy_env.db2.create_table(customer_table)
    orchestrator.legacy_env.db2.create_table(transaction_table)
    
    print(f"Created DB2 table: {customer_table.schema}.{customer_table.table_name}")
    print(f"Created DB2 table: {transaction_table.schema}.{transaction_table.table_name}")
    print()
    
    print("Step 2: Generating synthetic legacy data...")
    print("-" * 80)
    
    # Generate customer data
    customer_data = data_generator.generate_db2_customer_data(count=1000)
    orchestrator.legacy_env.db2.insert_data("LEGACY", "CUSTOMERS", customer_data)
    print(f"Generated and inserted {len(customer_data)} customer records")
    
    # Generate transaction data
    customer_ids = [c["CUSTOMER_ID"] for c in customer_data]
    transaction_data = data_generator.generate_db2_transaction_data(customer_ids, count=5000)
    orchestrator.legacy_env.db2.insert_data("LEGACY", "TRANSACTIONS", transaction_data)
    print(f"Generated and inserted {len(transaction_data)} transaction records")
    print()
    
    # Create VSAM files
    print("Step 3: Setting up VSAM files...")
    print("-" * 80)
    
    vsam_file = VSAMFile(
        file_name="CUSTOMER.MASTER",
        file_type=VSAMFileType.KSDS,
        record_length=200,
        key_offset=0,
        key_length=20
    )
    orchestrator.legacy_env.vsam.create_file(vsam_file)
    
    # Generate VSAM records
    vsam_records = data_generator.generate_vsam_record_data(record_length=200, count=500)
    for record in vsam_records:
        orchestrator.legacy_env.vsam.write_record("CUSTOMER.MASTER", record)
    
    print(f"Created VSAM file: {vsam_file.file_name} with {len(vsam_records)} records")
    print()
    
    print("Step 4: Preparing migration plan...")
    print("-" * 80)
    
    migration_plan = {
        "source_system": "DB2/VSAM Mainframe",
        "target_system": "PostgreSQL/Microservices",
        "estimated_records": len(customer_data) + len(transaction_data),
        "table_count": 2,
        "business_criticality": "HIGH",
        "max_downtime_hours": 4
    }
    
    print(f"Source System: {migration_plan['source_system']}")
    print(f"Target System: {migration_plan['target_system']}")
    print(f"Total Records to Migrate: {migration_plan['estimated_records']}")
    print(f"Business Criticality: {migration_plan['business_criticality']}")
    print()
    
    print("Step 5: Executing migration...")
    print("-" * 80)
    
    # Run the migration
    result = await orchestrator.run_migration(
        source="db2_legacy",
        target="postgresql_cloud",
        workflow="api_driven",
        migration_plan=migration_plan
    )
    
    print(f"\nMigration Status: {result.status.value}")
    print(f"Started at: {result.started_at}")
    print(f"Completed at: {result.completed_at}")
    print(f"Duration: {result.duration:.2f} seconds")
    print(f"Records Migrated: {result.records_migrated}")
    print()
    
    print("Step 6: Migration Phases Detail...")
    print("-" * 80)
    
    for i, phase in enumerate(result.phases, 1):
        phase_name = phase.get("phase", "Unknown")
        phase_status = phase.get("status", "Unknown")
        print(f"{i}. {phase_name}: {phase_status}")
        
        if "risk_assessment" in phase:
            risk = phase["risk_assessment"]
            print(f"   - Risk Level: {risk['risk_level']}")
            print(f"   - Risk Score: {risk['overall_risk_score']:.1f}/100")
            if risk.get("recommendations"):
                print(f"   - Recommendations: {len(risk['recommendations'])}")
        
        if "records_migrated" in phase:
            print(f"   - Records Migrated: {phase['records_migrated']}")
    
    print()
    
    print("Step 7: Validation Results...")
    print("-" * 80)
    
    # Get validation phase
    validation_phase = next(
        (p for p in result.phases if p.get("phase") == "validation"),
        None
    )
    
    if validation_phase and "validations" in validation_phase:
        for validation in validation_phase["validations"]:
            table = validation["table"]
            source = validation["source_count"]
            target = validation["target_count"]
            matched = "✓" if validation["matched"] else "✗"
            print(f"{matched} {table}: {source} → {target}")
    
    print()
    
    print("Step 8: Cloud Environment Status...")
    print("-" * 80)
    
    cloud_status = orchestrator.cloud_env.get_environment_status()
    print(f"Environment Type: {cloud_status['environment_type']}")
    print(f"PostgreSQL Tables: {cloud_status['postgresql_tables']}")
    print(f"Microservices: {cloud_status['microservices']}")
    print()
    
    print("=" * 80)
    print("Migration Simulation Completed Successfully!")
    print("=" * 80)
    
    return result


if __name__ == "__main__":
    # Run the complete migration example
    result = asyncio.run(run_complete_migration_example())
