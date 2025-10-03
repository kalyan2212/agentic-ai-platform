# Quick Start Guide

## Get Up and Running in 5 Minutes

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/kalyan2212/agentic-ai-platform.git
cd agentic-ai-platform

# 2. Install dependencies
pip install -r requirements.txt
```

### Run Your First Migration

```bash
# Run the complete migration example
PYTHONPATH=. python examples/complete_migration.py
```

**Expected output:**
```
Migration Status: completed
Records Migrated: 6000
Duration: 0.02 seconds
All validations passed ✓
```

### Run All Tests

```bash
# Run all 34 tests
python -m pytest tests/ -v
```

**Expected output:**
```
34 passed in 0.18s
```

### Try Different Workflows

```bash
# EDI/B2B Migration
PYTHONPATH=. python examples/edi_migration.py

# Microservices Migration (CICS to REST API)
PYTHONPATH=. python examples/microservices_migration.py
```

### Run Benchmarks

```bash
# Performance benchmarking
PYTHONPATH=. python tests/benchmarks/run_benchmarks.py
```

**Expected output:**
```
Benchmark Results:
- Small (1K):   455,556 records/second
- Medium (10K): 612,620 records/second
- Large (100K): 643,667 records/second
```

### Create Your Own Migration

```python
import asyncio
from src.migration.orchestrator import MigrationOrchestrator
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType

async def main():
    orchestrator = MigrationOrchestrator()
    
    # Create your table
    table = DB2Table(
        schema="MYSCHEMA",
        table_name="MYTABLE",
        columns=[
            DB2Column("ID", DB2DataType.INTEGER),
            DB2Column("NAME", DB2DataType.VARCHAR, length=100)
        ],
        primary_key=["ID"]
    )
    orchestrator.legacy_env.db2.create_table(table)
    
    # Add data
    orchestrator.legacy_env.db2.insert_data("MYSCHEMA", "MYTABLE", [
        {"ID": 1, "NAME": "Test"}
    ])
    
    # Run migration
    result = await orchestrator.run_migration(
        source="db2_legacy",
        target="postgresql_cloud",
        workflow="api_driven"
    )
    
    print(f"Status: {result.status.value}")
    print(f"Records: {result.records_migrated}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Learn More

- 📖 [User Guide](docs/user_guide.md) - Detailed usage guide
- 🏗️ [Architecture](docs/architecture.md) - System design
- 📚 [API Documentation](docs/api_documentation.md) - Complete API reference
- 📄 [Patent Specification](docs/patent_specification.md) - Innovations

### Need Help?

- Check [Technical Documentation](docs/technical_documentation.md)
- Review [Project Summary](PROJECT_SUMMARY.md)
- See working examples in `examples/` directory

---

**Ready to migrate!** 🚀
