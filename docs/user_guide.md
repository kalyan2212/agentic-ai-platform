# User Guide - Enterprise Agentic Migration Platform

## Quick Start Guide

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/kalyan2212/agentic-ai-platform.git
cd agentic-ai-platform
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running Your First Migration Simulation

#### Example 1: Complete End-to-End Migration

```bash
python examples/complete_migration.py
```

This example demonstrates:
- Setting up a legacy DB2/VSAM environment
- Generating synthetic customer and transaction data
- Running a complete migration to PostgreSQL
- Validating the migration results

**Expected Output:**
```
================================================================================
Enterprise Agentic Migration Platform - Complete Migration Example
================================================================================

Step 1: Setting up legacy mainframe environment...
--------------------------------------------------------------------------------
Created DB2 table: LEGACY.CUSTOMERS
Created DB2 table: LEGACY.TRANSACTIONS

Step 2: Generating synthetic legacy data...
--------------------------------------------------------------------------------
Generated and inserted 1000 customer records
Generated and inserted 5000 transaction records

...

Migration Status: completed
Records Migrated: 6000
Duration: X.XX seconds
```

### Understanding the Output

#### Migration Phases

1. **Analysis Phase**: 
   - Exports legacy environment
   - Analyzes schema complexity
   - Identifies optimization opportunities

2. **Risk Assessment Phase**:
   - Evaluates migration risk (0-100 score)
   - Classifies risk level (LOW/MEDIUM/HIGH)
   - Provides mitigation recommendations

3. **Schema Mapping Phase**:
   - Maps DB2 tables to PostgreSQL
   - Converts data types
   - Optimizes schema design

4. **Data Migration Phase**:
   - Extracts data from legacy systems
   - Transforms data formats
   - Loads into target systems

5. **Validation Phase**:
   - Compares record counts
   - Validates data integrity
   - Reports success/failure

### Custom Migration Scenarios

#### Example 2: Creating a Custom Migration

```python
from src.migration.orchestrator import MigrationOrchestrator
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType
from src.data_generators.synthetic_data import SyntheticDataGenerator

# Initialize orchestrator
orchestrator = MigrationOrchestrator()

# Create your own table structure
my_table = DB2Table(
    schema="MYSCHEMA",
    table_name="MYTABLE",
    columns=[
        DB2Column("ID", DB2DataType.INTEGER),
        DB2Column("NAME", DB2DataType.VARCHAR, length=100),
        DB2Column("AMOUNT", DB2DataType.DECIMAL, precision=10, scale=2)
    ],
    primary_key=["ID"]
)

# Register table
orchestrator.legacy_env.db2.create_table(my_table)

# Generate data
generator = SyntheticDataGenerator(seed=42)
# ... add your data generation logic

# Run migration
import asyncio
result = asyncio.run(orchestrator.run_migration(
    source="db2_legacy",
    target="postgresql_cloud",
    workflow="batch"
))

print(f"Migration completed: {result.status}")
```

## Advanced Usage

### Working with Different Workflows

The platform supports multiple migration workflows:

1. **API-Driven Migration**: For REST API-based data transfer
2. **Batch Migration**: For large batch processing scenarios
3. **EDI Migration**: For EDI/B2B integration patterns
4. **Thick Client Migration**: For client-server applications

```python
# API-driven workflow
result = await orchestrator.run_migration(
    source="db2_legacy",
    target="postgresql_cloud",
    workflow="api_driven"
)

# Batch workflow
result = await orchestrator.run_migration(
    source="db2_legacy",
    target="postgresql_cloud",
    workflow="batch"
)
```

### Customizing Migration Plans

```python
migration_plan = {
    "source_system": "DB2/VSAM Mainframe",
    "target_system": "PostgreSQL/Microservices",
    "estimated_records": 10000000,  # 10 million records
    "table_count": 50,
    "business_criticality": "CRITICAL",
    "max_downtime_hours": 2
}

result = await orchestrator.run_migration(
    source="db2_legacy",
    target="postgresql_cloud",
    workflow="api_driven",
    migration_plan=migration_plan
)
```

### Working with VSAM Files

```python
from src.legacy.mainframe_simulator import VSAMFile, VSAMFileType

# Create VSAM file
vsam_file = VSAMFile(
    file_name="MY.DATA.FILE",
    file_type=VSAMFileType.KSDS,
    record_length=256,
    key_offset=0,
    key_length=20
)

orchestrator.legacy_env.vsam.create_file(vsam_file)

# Write records
data = b"A" * 256
orchestrator.legacy_env.vsam.write_record("MY.DATA.FILE", data)
```

### Working with COBOL Programs

```python
from src.legacy.mainframe_simulator import COBOLProgram

# Register COBOL program
program = COBOLProgram(
    program_name="MYBATCH",
    source_code="IDENTIFICATION DIVISION...",
    input_files=["INPUT.DAT"],
    output_files=["OUTPUT.DAT"]
)

orchestrator.legacy_env.cobol.register_program(program)

# Execute program
result = orchestrator.legacy_env.cobol.execute_program(
    "MYBATCH",
    {"param1": "value1"}
)
```

### Working with CICS Transactions

```python
from src.legacy.mainframe_simulator import CICSProgram, CICSTransaction

# Register CICS program
program = CICSProgram(
    program_id="INQ001",
    transaction_code="INQ1",
    supported_transactions=[CICSTransaction.INQUIRY]
)

orchestrator.legacy_env.cics.register_program(program)

# Execute transaction
result = orchestrator.legacy_env.cics.execute_transaction(
    "INQ1",
    CICSTransaction.INQUIRY,
    {"customer_id": "12345"}
)
```

## Monitoring and Logging

The platform uses structured logging. To view detailed logs:

```python
import structlog
import logging

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Logs will show:
# - Agent activities
# - Migration phases
# - Data operations
# - Risk assessments
# - Validation results
```

## Testing

### Running Unit Tests

```bash
pytest tests/unit/
```

### Running Specific Tests

```bash
# Test orchestration
pytest tests/unit/test_orchestration.py

# Test legacy simulator
pytest tests/unit/test_legacy_simulator.py

# Test data generators
pytest tests/unit/test_synthetic_data.py
```

### Running Tests with Coverage

```bash
pytest --cov=src tests/
```

## Troubleshooting

### Common Issues

**Issue**: Import errors
```bash
# Solution: Ensure you're in the project root
cd /path/to/agentic-ai-platform
python -m pytest tests/
```

**Issue**: Missing dependencies
```bash
# Solution: Reinstall requirements
pip install -r requirements.txt --upgrade
```

**Issue**: Async errors
```python
# Solution: Always use asyncio.run() for async functions
import asyncio
result = asyncio.run(orchestrator.run_migration(...))
```

## Best Practices

1. **Use Seeds for Reproducibility**: Always set a seed for synthetic data generation in tests
   ```python
   generator = SyntheticDataGenerator(seed=42)
   ```

2. **Monitor Risk Scores**: Pay attention to risk assessment recommendations
   ```python
   for recommendation in risk_assessment["recommendations"]:
       print(f"⚠️  {recommendation}")
   ```

3. **Validate Migration Results**: Always check validation phase output
   ```python
   for validation in validation_phase["validations"]:
       if not validation["matched"]:
           print(f"⚠️  Validation failed for {validation['table']}")
   ```

4. **Use Appropriate Workflows**: Choose workflow based on migration scenario
   - `api_driven`: Real-time, transactional data
   - `batch`: Large bulk data transfers
   - `edi`: B2B integration scenarios
   - `thick_client`: Client-server migrations

## API Reference

See [API Documentation](api_documentation.md) for detailed API reference.

## Examples

All examples are in the `examples/` directory:

- `complete_migration.py`: Full end-to-end migration simulation
- More examples coming soon...

## Support

For issues and questions:
- Check the [Technical Documentation](technical_documentation.md)
- Review [Architecture Blueprint](architecture.md)
- See [Patent Specification](patent_specification.md) for innovation details

## Next Steps

1. Review the [Architecture Blueprint](architecture.md) to understand system design
2. Explore the [Patent Specification](patent_specification.md) for innovation details
3. Run the complete migration example
4. Create your own custom migration scenarios
5. Experiment with different workflows and data patterns
