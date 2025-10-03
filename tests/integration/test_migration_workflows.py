"""
Integration tests for end-to-end migration workflows
"""

import pytest
import asyncio

from src.migration.orchestrator import MigrationOrchestrator, MigrationStatus
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType
from src.data_generators.synthetic_data import SyntheticDataGenerator


@pytest.mark.asyncio
async def test_complete_db2_to_postgresql_migration():
    """Test complete DB2 to PostgreSQL migration"""
    orchestrator = MigrationOrchestrator()
    generator = SyntheticDataGenerator(seed=42)
    
    # Create DB2 table
    table = DB2Table(
        schema="TEST",
        table_name="USERS",
        columns=[
            DB2Column("USER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("USERNAME", DB2DataType.VARCHAR, length=50),
            DB2Column("EMAIL", DB2DataType.VARCHAR, length=100)
        ],
        primary_key=["USER_ID"]
    )
    
    orchestrator.legacy_env.db2.create_table(table)
    
    # Insert test data
    test_data = [
        {"USER_ID": "U001", "USERNAME": "alice", "EMAIL": "alice@example.com"},
        {"USER_ID": "U002", "USERNAME": "bob", "EMAIL": "bob@example.com"}
    ]
    
    orchestrator.legacy_env.db2.insert_data("TEST", "USERS", test_data)
    
    # Run migration
    result = await orchestrator.run_migration(
        source="db2_test",
        target="postgresql_test",
        workflow="api_driven"
    )
    
    # Assertions
    assert result.status == MigrationStatus.COMPLETED
    assert result.records_migrated == 2
    assert result.duration is not None
    assert len(result.phases) == 5  # Risk, Analysis, Mapping, Migration, Validation


@pytest.mark.asyncio
async def test_multi_table_migration():
    """Test migration with multiple tables"""
    orchestrator = MigrationOrchestrator()
    
    # Create multiple tables
    for i in range(3):
        table = DB2Table(
            schema="MULTI",
            table_name=f"TABLE_{i}",
            columns=[
                DB2Column("ID", DB2DataType.INTEGER),
                DB2Column("DATA", DB2DataType.VARCHAR, length=50)
            ],
            primary_key=["ID"]
        )
        
        orchestrator.legacy_env.db2.create_table(table)
        
        # Insert data
        data = [{"ID": j, "DATA": f"Data_{i}_{j}"} for j in range(10)]
        orchestrator.legacy_env.db2.insert_data("MULTI", f"TABLE_{i}", data)
    
    # Run migration
    result = await orchestrator.run_migration(
        source="db2_multi",
        target="postgresql_multi",
        workflow="batch"
    )
    
    # Assertions
    assert result.status == MigrationStatus.COMPLETED
    assert result.records_migrated == 30  # 3 tables × 10 records


@pytest.mark.asyncio
async def test_migration_with_risk_assessment():
    """Test that risk assessment is performed"""
    orchestrator = MigrationOrchestrator()
    
    # Create table
    table = DB2Table(
        schema="RISK",
        table_name="DATA",
        columns=[
            DB2Column("ID", DB2DataType.INTEGER),
            DB2Column("VALUE", DB2DataType.VARCHAR, length=100)
        ]
    )
    
    orchestrator.legacy_env.db2.create_table(table)
    orchestrator.legacy_env.db2.insert_data("RISK", "DATA", [
        {"ID": 1, "VALUE": "Test"}
    ])
    
    # Run migration with plan
    migration_plan = {
        "estimated_records": 1000000,
        "table_count": 100,
        "business_criticality": "CRITICAL",
        "max_downtime_hours": 1
    }
    
    result = await orchestrator.run_migration(
        source="db2_risk",
        target="postgresql_risk",
        workflow="batch",
        migration_plan=migration_plan
    )
    
    # Check that risk assessment was performed
    risk_phase = next(
        (p for p in result.phases if p.get("phase") == "analysis" and "risk_assessment" in p),
        None
    )
    
    assert risk_phase is not None
    assert "risk_assessment" in risk_phase
    assert "risk_level" in risk_phase["risk_assessment"]
    assert "overall_risk_score" in risk_phase["risk_assessment"]


@pytest.mark.asyncio
async def test_data_validation():
    """Test that data validation is performed correctly"""
    orchestrator = MigrationOrchestrator()
    
    # Create and populate table
    table = DB2Table(
        schema="VALID",
        table_name="RECORDS",
        columns=[
            DB2Column("ID", DB2DataType.INTEGER),
            DB2Column("NAME", DB2DataType.VARCHAR, length=50)
        ]
    )
    
    orchestrator.legacy_env.db2.create_table(table)
    
    records = [{"ID": i, "NAME": f"Name_{i}"} for i in range(100)]
    orchestrator.legacy_env.db2.insert_data("VALID", "RECORDS", records)
    
    # Run migration
    result = await orchestrator.run_migration(
        source="db2_valid",
        target="postgresql_valid",
        workflow="api_driven"
    )
    
    # Get validation phase
    validation_phase = next(
        (p for p in result.phases if p.get("phase") == "validation"),
        None
    )
    
    assert validation_phase is not None
    assert "validations" in validation_phase
    
    # Check that all validations passed
    validations = validation_phase["validations"]
    assert len(validations) > 0
    assert all(v["matched"] for v in validations)


@pytest.mark.asyncio
async def test_schema_mapping():
    """Test schema mapping from DB2 to PostgreSQL"""
    orchestrator = MigrationOrchestrator()
    
    # Create DB2 table with various data types
    table = DB2Table(
        schema="SCHEMA",
        table_name="TYPES",
        columns=[
            DB2Column("COL_VARCHAR", DB2DataType.VARCHAR, length=100),
            DB2Column("COL_INTEGER", DB2DataType.INTEGER),
            DB2Column("COL_DECIMAL", DB2DataType.DECIMAL, precision=10, scale=2),
            DB2Column("COL_DATE", DB2DataType.DATE),
            DB2Column("COL_CHAR", DB2DataType.CHAR, length=10)
        ]
    )
    
    orchestrator.legacy_env.db2.create_table(table)
    orchestrator.legacy_env.db2.insert_data("SCHEMA", "TYPES", [
        {
            "COL_VARCHAR": "test",
            "COL_INTEGER": 123,
            "COL_DECIMAL": 456.78,
            "COL_DATE": "2024-01-01",
            "COL_CHAR": "CHAR      "  # Padded
        }
    ])
    
    # Run migration
    result = await orchestrator.run_migration(
        source="db2_schema",
        target="postgresql_schema",
        workflow="batch"
    )
    
    # Check that PostgreSQL table was created
    pg_table = orchestrator.cloud_env.postgresql.tables.get("schema.types")
    assert pg_table is not None
    assert pg_table.schema == "schema"  # Lowercase
    assert pg_table.table_name == "types"  # Lowercase
    
    # Check data transformation
    pg_data = orchestrator.cloud_env.postgresql.select_data("schema", "types")
    assert len(pg_data) == 1
    assert pg_data[0]["col_char"] == "CHAR"  # Trimmed


def test_agent_registration():
    """Test agent registration and discovery"""
    orchestrator = MigrationOrchestrator()
    
    # Check that default agents are registered
    assert len(orchestrator.orchestration_engine.agents) > 0
    
    # Check for specific agent types
    agent_ids = list(orchestrator.orchestration_engine.agents.keys())
    assert "analyzer_1" in agent_ids
    assert "mapper_1" in agent_ids
    assert "migrator_1" in agent_ids
    assert "validator_1" in agent_ids


@pytest.mark.asyncio
async def test_different_workflows():
    """Test different migration workflows"""
    workflows = ["api_driven", "batch", "edi"]
    
    for workflow in workflows:
        orchestrator = MigrationOrchestrator()
        
        # Create simple table
        table = DB2Table(
            schema="FLOW",
            table_name=f"DATA_{workflow.upper()}",
            columns=[
                DB2Column("ID", DB2DataType.INTEGER),
                DB2Column("VALUE", DB2DataType.VARCHAR, length=50)
            ]
        )
        
        orchestrator.legacy_env.db2.create_table(table)
        orchestrator.legacy_env.db2.insert_data(
            "FLOW",
            f"DATA_{workflow.upper()}",
            [{"ID": 1, "VALUE": "test"}]
        )
        
        # Run migration with specific workflow
        result = await orchestrator.run_migration(
            source="db2_flow",
            target="postgresql_flow",
            workflow=workflow
        )
        
        # Check that migration completed
        assert result.status == MigrationStatus.COMPLETED
        assert result.records_migrated == 1
        
        # Check that workflow was recorded
        migration_phase = next(
            (p for p in result.phases if p.get("phase") == "data_loading"),
            None
        )
        assert migration_phase is not None
        assert migration_phase.get("workflow") == workflow
