"""
Example: Microservices API Migration

Demonstrates migrating from CICS transactions to REST API microservices.
"""

import asyncio

from src.migration.orchestrator import MigrationOrchestrator
from src.legacy.mainframe_simulator import CICSProgram, CICSTransaction, DB2Table, DB2Column, DB2DataType
from src.cloud.cloud_native_simulator import APIEndpoint, HTTPMethod
from src.data_generators.synthetic_data import SyntheticDataGenerator


async def run_microservices_migration_example():
    """Run a CICS to microservices migration simulation"""
    
    print("=" * 80)
    print("Microservices API Migration - CICS to REST API")
    print("=" * 80)
    print()
    
    # Initialize components
    orchestrator = MigrationOrchestrator()
    data_generator = SyntheticDataGenerator(seed=200)
    
    print("Step 1: Setting up legacy CICS environment...")
    print("-" * 80)
    
    # Create customer table in DB2
    customer_table = DB2Table(
        schema="ONLINE",
        table_name="CUSTOMERS",
        columns=[
            DB2Column("CUSTOMER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("NAME", DB2DataType.VARCHAR, length=100),
            DB2Column("EMAIL", DB2DataType.VARCHAR, length=100),
            DB2Column("PHONE", DB2DataType.VARCHAR, length=20),
            DB2Column("STATUS", DB2DataType.VARCHAR, length=20)
        ],
        primary_key=["CUSTOMER_ID"]
    )
    
    orchestrator.legacy_env.db2.create_table(customer_table)
    
    # Register CICS programs
    inquiry_program = CICSProgram(
        program_id="CUSINQ01",
        transaction_code="CINQ",
        supported_transactions=[CICSTransaction.INQUIRY]
    )
    
    update_program = CICSProgram(
        program_id="CUSUPD01",
        transaction_code="CUPD",
        supported_transactions=[CICSTransaction.UPDATE]
    )
    
    orchestrator.legacy_env.cics.register_program(inquiry_program)
    orchestrator.legacy_env.cics.register_program(update_program)
    
    print(f"Registered CICS program: {inquiry_program.program_id} (Transaction: {inquiry_program.transaction_code})")
    print(f"Registered CICS program: {update_program.program_id} (Transaction: {update_program.transaction_code})")
    print()
    
    print("Step 2: Generating customer data...")
    print("-" * 80)
    
    customers = data_generator.generate_db2_customer_data(count=500)
    orchestrator.legacy_env.db2.insert_data("ONLINE", "CUSTOMERS", customers)
    print(f"Generated {len(customers)} customer records")
    print()
    
    print("Step 3: Simulating CICS transactions...")
    print("-" * 80)
    
    # Simulate some CICS transactions
    for i in range(5):
        customer_id = customers[i]["CUSTOMER_ID"]
        
        # Inquiry transaction
        result = orchestrator.legacy_env.cics.execute_transaction(
            "CINQ",
            CICSTransaction.INQUIRY,
            {"customer_id": customer_id}
        )
        print(f"  CICS CINQ: Customer {customer_id} - {result['status']}")
    
    print(f"\nTotal CICS transactions logged: {len(orchestrator.legacy_env.cics.transaction_log)}")
    print()
    
    print("Step 4: Creating cloud microservices...")
    print("-" * 80)
    
    # Create customer microservice
    customer_service = orchestrator.cloud_env.create_microservice("customer-service")
    
    # Register REST API endpoints
    endpoints = [
        APIEndpoint(
            path="/api/v1/customers/{id}",
            method=HTTPMethod.GET,
            service_name="customer-service",
            request_schema={"id": "string"},
            response_schema={"customer": "object"}
        ),
        APIEndpoint(
            path="/api/v1/customers/{id}",
            method=HTTPMethod.PUT,
            service_name="customer-service",
            request_schema={"id": "string", "data": "object"},
            response_schema={"customer": "object"}
        ),
        APIEndpoint(
            path="/api/v1/customers",
            method=HTTPMethod.POST,
            service_name="customer-service",
            request_schema={"customer": "object"},
            response_schema={"customer": "object"}
        )
    ]
    
    for endpoint in endpoints:
        customer_service.register_endpoint(endpoint)
        print(f"  Registered: {endpoint.method.value} {endpoint.path}")
    
    print()
    
    print("Step 5: Running migration...")
    print("-" * 80)
    
    migration_plan = {
        "source_system": "CICS/DB2 Online",
        "target_system": "REST API Microservices",
        "estimated_records": len(customers),
        "table_count": 1,
        "business_criticality": "HIGH",
        "max_downtime_hours": 2
    }
    
    result = await orchestrator.run_migration(
        source="cics_online",
        target="microservices_api",
        workflow="api_driven",
        migration_plan=migration_plan
    )
    
    print(f"\nMigration Status: {result.status.value}")
    print(f"Records Migrated: {result.records_migrated}")
    print(f"Duration: {result.duration:.2f} seconds")
    print()
    
    print("Step 6: Testing REST API endpoints...")
    print("-" * 80)
    
    # Test API calls
    migrated_customers = orchestrator.cloud_env.postgresql.select_data("online", "customers")
    
    for i in range(3):
        customer = migrated_customers[i]
        customer_id = customer.get("customer_id")
        
        # GET request - using the generic path since we're simulating
        response = customer_service.handle_request(
            HTTPMethod.GET,
            "/api/v1/customers/{id}",
            {"id": customer_id}
        )
        
        print(f"  GET /api/v1/customers/{customer_id}")
        print(f"    Status: {response['status']}")
        if response['status'] == 200:
            print(f"    Response: {response['data']['message']}")
        else:
            print(f"    Note: Simulated endpoint - actual implementation would query PostgreSQL")
    
    print()
    
    print("Step 7: Microservices metrics...")
    print("-" * 80)
    
    print(f"Microservices deployed: {len(orchestrator.cloud_env.microservices)}")
    print(f"Total API endpoints: {len(customer_service.endpoints)}")
    print(f"API requests handled: {len(customer_service.request_log)}")
    print()
    
    print("Step 8: Comparison - Legacy vs Cloud...")
    print("-" * 80)
    
    print("Legacy CICS:")
    print(f"  - Transaction programs: {len(orchestrator.legacy_env.cics.programs)}")
    print(f"  - Transactions executed: {len(orchestrator.legacy_env.cics.transaction_log)}")
    print(f"  - Interface: Green screen terminals")
    print()
    
    print("Cloud Microservices:")
    print(f"  - Microservices: {len(orchestrator.cloud_env.microservices)}")
    print(f"  - REST API endpoints: {len(customer_service.endpoints)}")
    print(f"  - API calls: {len(customer_service.request_log)}")
    print(f"  - Interface: RESTful APIs (JSON)")
    print()
    
    print("=" * 80)
    print("Microservices Migration Completed Successfully!")
    print("=" * 80)
    print()
    print("Summary:")
    print(f"  - CICS programs migrated: 2")
    print(f"  - Customer records migrated: {result.records_migrated}")
    print(f"  - REST API endpoints created: {len(endpoints)}")
    print(f"  - Migration workflow: api_driven")
    print(f"  - Migration duration: {result.duration:.2f} seconds")
    
    return result


if __name__ == "__main__":
    result = asyncio.run(run_microservices_migration_example())
