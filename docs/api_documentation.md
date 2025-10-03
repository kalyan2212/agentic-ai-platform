# API Documentation

## Enterprise Agentic Migration Platform - API Reference

---

## Table of Contents

1. [Orchestration API](#orchestration-api)
2. [Legacy Simulators API](#legacy-simulators-api)
3. [Cloud-Native API](#cloud-native-api)
4. [Data Generation API](#data-generation-api)
5. [Migration API](#migration-api)

---

## Orchestration API

### OrchestrationEngine

Main coordinator for all agent activities.

#### Methods

##### `register_agent(agent: BaseAgent) -> None`

Register a new agent with the orchestration engine.

**Parameters:**
- `agent` (BaseAgent): Agent instance to register

**Example:**
```python
from src.agents.orchestration import OrchestrationEngine, BaseAgent, AgentRole

engine = OrchestrationEngine()
agent = BaseAgent("custom_agent", AgentRole.DATA_ANALYZER, ["analyze"])
engine.register_agent(agent)
```

##### `async route_message(message: AgentMessage) -> None`

Route message to appropriate agent based on capability and workload.

**Parameters:**
- `message` (AgentMessage): Message to route

**Example:**
```python
message = AgentMessage(
    sender="coordinator",
    receiver="analyzer_1",
    message_type="analyze_schema",
    content={"schema": schema_data}
)
await engine.route_message(message)
```

##### `async achieve_consensus(decision: Dict[str, Any]) -> bool`

Coordinate multi-agent voting for critical decisions.

**Parameters:**
- `decision` (Dict): Decision to vote on

**Returns:**
- `bool`: True if consensus achieved (≥66% approval)

**Example:**
```python
decision = {
    "type": "schema_change",
    "description": "Modify table schema",
    "impact": "MEDIUM"
}
consensus = await engine.achieve_consensus(decision)
```

##### `async resolve_conflict(conflict: Dict[str, Any]) -> Dict[str, Any]`

Resolve conflicts using agent negotiation protocols.

**Parameters:**
- `conflict` (Dict): Conflict description

**Returns:**
- `Dict`: Resolution details

**Example:**
```python
conflict = {
    "type": "schema_mapping",
    "source": "DB2_TABLE",
    "target": "PG_TABLE"
}
resolution = await engine.resolve_conflict(conflict)
```

---

## Legacy Simulators API

### DB2Simulator

Simulates IBM DB2 mainframe database.

#### Methods

##### `create_table(table: DB2Table) -> None`

Create a DB2 table.

**Parameters:**
- `table` (DB2Table): Table definition

**Example:**
```python
from src.legacy.mainframe_simulator import DB2Simulator, DB2Table, DB2Column, DB2DataType

db2 = DB2Simulator()
table = DB2Table(
    schema="PROD",
    table_name="CUSTOMERS",
    columns=[
        DB2Column("CUSTOMER_ID", DB2DataType.VARCHAR, length=20),
        DB2Column("NAME", DB2DataType.VARCHAR, length=100)
    ],
    primary_key=["CUSTOMER_ID"]
)
db2.create_table(table)
```

##### `insert_data(schema: str, table_name: str, records: List[Dict[str, Any]]) -> None`

Insert records into table.

**Parameters:**
- `schema` (str): Schema name
- `table_name` (str): Table name
- `records` (List[Dict]): Records to insert

**Example:**
```python
db2.insert_data("PROD", "CUSTOMERS", [
    {"CUSTOMER_ID": "C001", "NAME": "John Doe"},
    {"CUSTOMER_ID": "C002", "NAME": "Jane Smith"}
])
```

##### `select_data(schema: str, table_name: str, where_clause: Optional[Dict] = None) -> List[Dict[str, Any]]`

Select records from table.

**Parameters:**
- `schema` (str): Schema name
- `table_name` (str): Table name
- `where_clause` (Optional[Dict]): Filter conditions

**Returns:**
- `List[Dict]`: Selected records

**Example:**
```python
# Select all
all_customers = db2.select_data("PROD", "CUSTOMERS")

# Select with filter
active = db2.select_data("PROD", "CUSTOMERS", {"STATUS": "ACTIVE"})
```

### VSAMSimulator

Simulates VSAM file system.

#### Methods

##### `create_file(vsam_file: VSAMFile) -> None`

Create a VSAM file.

**Example:**
```python
from src.legacy.mainframe_simulator import VSAMSimulator, VSAMFile, VSAMFileType

vsam = VSAMSimulator()
vsam_file = VSAMFile(
    file_name="MASTER.DATA",
    file_type=VSAMFileType.KSDS,
    record_length=256,
    key_offset=0,
    key_length=10
)
vsam.create_file(vsam_file)
```

##### `write_record(file_name: str, record: bytes) -> None`

Write fixed-length record to VSAM file.

**Example:**
```python
record = b"KEY0001234" + b"DATA" * 60
vsam.write_record("MASTER.DATA", record)
```

---

## Cloud-Native API

### PostgreSQLSimulator

Simulates PostgreSQL database.

#### Methods

##### `create_table(table: PostgreSQLTable) -> None`

Create a PostgreSQL table.

**Example:**
```python
from src.cloud.cloud_native_simulator import PostgreSQLSimulator, PostgreSQLTable, PostgreSQLColumn, PostgreSQLDataType

pg = PostgreSQLSimulator()
table = PostgreSQLTable(
    schema="public",
    table_name="customers",
    columns=[
        PostgreSQLColumn("customer_id", PostgreSQLDataType.VARCHAR, length=20),
        PostgreSQLColumn("name", PostgreSQLDataType.VARCHAR, length=100),
        PostgreSQLColumn("metadata", PostgreSQLDataType.JSONB)
    ],
    primary_key=["customer_id"]
)
pg.create_table(table)
```

### MicroserviceSimulator

Simulates REST API microservices.

#### Methods

##### `register_endpoint(endpoint: APIEndpoint) -> None`

Register a REST API endpoint.

**Example:**
```python
from src.cloud.cloud_native_simulator import MicroserviceSimulator, APIEndpoint, HTTPMethod

service = MicroserviceSimulator("customer-service")
endpoint = APIEndpoint(
    path="/api/v1/customers/{id}",
    method=HTTPMethod.GET,
    service_name="customer-service",
    request_schema={"id": "string"},
    response_schema={"customer": "object"}
)
service.register_endpoint(endpoint)
```

##### `handle_request(method: HTTPMethod, path: str, data: Dict[str, Any]) -> Dict[str, Any]`

Handle an API request.

**Example:**
```python
response = service.handle_request(
    HTTPMethod.GET,
    "/api/v1/customers/{id}",
    {"id": "C001"}
)
```

### EDISimulator

Simulates EDI/B2B message exchange.

#### Methods

##### `send_message(message: EDIMessage) -> None`

Send an EDI message.

**Example:**
```python
from src.cloud.cloud_native_simulator import EDISimulator, EDIMessage, EDIMessageType

edi = EDISimulator()
message = EDIMessage(
    message_type=EDIMessageType.ORDERS,
    sender_id="BUYER001",
    receiver_id="SELLER001",
    control_number="PO20240001",
    data={"order_items": [...]}
)
edi.send_message(message)
```

---

## Data Generation API

### SyntheticDataGenerator

Generates realistic synthetic data for testing.

#### Methods

##### `generate_db2_customer_data(count: int) -> List[Dict[str, Any]]`

Generate customer data in DB2 format.

**Parameters:**
- `count` (int): Number of records to generate

**Returns:**
- `List[Dict]`: Customer records

**Example:**
```python
from src.data_generators.synthetic_data import SyntheticDataGenerator

generator = SyntheticDataGenerator(seed=42)
customers = generator.generate_db2_customer_data(count=1000)
```

##### `generate_db2_transaction_data(customer_ids: List[str], count: int) -> List[Dict[str, Any]]`

Generate transaction data with foreign key references.

**Example:**
```python
customer_ids = [c["CUSTOMER_ID"] for c in customers]
transactions = generator.generate_db2_transaction_data(customer_ids, count=5000)
```

##### `generate_edi_order_data(count: int) -> List[Dict[str, Any]]`

Generate EDI order data.

**Example:**
```python
orders = generator.generate_edi_order_data(count=100)
```

### DataMappingEngine

Intelligent schema and data transformation.

#### Methods

##### `map_db2_to_postgresql_table(db2_table: DB2Table) -> PostgreSQLTable`

Map DB2 table structure to PostgreSQL.

**Example:**
```python
from src.data_generators.synthetic_data import DataMappingEngine

mapper = DataMappingEngine()
pg_table = mapper.map_db2_to_postgresql_table(db2_table)
```

##### `transform_data_record(record: Dict[str, Any], source_table: DB2Table, target_table: PostgreSQLTable) -> Dict[str, Any]`

Transform a single data record.

**Example:**
```python
transformed = mapper.transform_data_record(
    db2_record,
    db2_table,
    pg_table
)
```

---

## Migration API

### MigrationOrchestrator

Coordinates complete migration workflow.

#### Methods

##### `async run_migration(source: str, target: str, workflow: str, migration_plan: Optional[Dict[str, Any]] = None) -> MigrationResult`

Run complete end-to-end migration.

**Parameters:**
- `source` (str): Source system identifier
- `target` (str): Target system identifier
- `workflow` (str): Migration workflow type ("api_driven", "batch", "edi")
- `migration_plan` (Optional[Dict]): Migration configuration

**Returns:**
- `MigrationResult`: Migration results

**Example:**
```python
from src.migration.orchestrator import MigrationOrchestrator

orchestrator = MigrationOrchestrator()

migration_plan = {
    "estimated_records": 1000000,
    "table_count": 25,
    "business_criticality": "HIGH",
    "max_downtime_hours": 4
}

result = await orchestrator.run_migration(
    source="db2_legacy",
    target="postgresql_cloud",
    workflow="api_driven",
    migration_plan=migration_plan
)

print(f"Status: {result.status}")
print(f"Records: {result.records_migrated}")
print(f"Duration: {result.duration}s")
```

### RiskAssessmentEngine

Evaluates migration risks.

#### Methods

##### `assess_migration_risk(migration_plan: Dict[str, Any]) -> Dict[str, Any]`

Assess risk level for migration.

**Parameters:**
- `migration_plan` (Dict): Migration plan details

**Returns:**
- `Dict`: Risk assessment results

**Example:**
```python
from src.migration.orchestrator import RiskAssessmentEngine

risk_engine = RiskAssessmentEngine()
assessment = risk_engine.assess_migration_risk({
    "estimated_records": 5000000,
    "table_count": 75,
    "business_criticality": "CRITICAL",
    "max_downtime_hours": 2
})

print(f"Risk Level: {assessment['risk_level']}")
print(f"Risk Score: {assessment['overall_risk_score']}")
```

### RollbackManager

Manages environment snapshots and recovery.

#### Methods

##### `create_snapshot(environment_state: Dict[str, Any]) -> str`

Create a snapshot of current environment state.

**Returns:**
- `str`: Snapshot ID

**Example:**
```python
from src.migration.orchestrator import RollbackManager

rollback_mgr = RollbackManager()
snapshot_id = rollback_mgr.create_snapshot(current_state)
```

##### `async execute_rollback(snapshot_id: str) -> Dict[str, Any]`

Execute rollback to a specific snapshot.

**Example:**
```python
result = await rollback_mgr.execute_rollback(snapshot_id)
```

---

## Data Types and Enums

### AgentRole

```python
class AgentRole(Enum):
    COORDINATOR = "coordinator"
    DATA_ANALYZER = "data_analyzer"
    SCHEMA_MAPPER = "schema_mapper"
    DATA_MIGRATOR = "data_migrator"
    VALIDATOR = "validator"
    RISK_ASSESSOR = "risk_assessor"
    ROLLBACK_MANAGER = "rollback_manager"
```

### MigrationStatus

```python
class MigrationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
```

### DB2DataType

```python
class DB2DataType(Enum):
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"
    SMALLINT = "SMALLINT"
    BIGINT = "BIGINT"
```

### PostgreSQLDataType

```python
class PostgreSQLDataType(Enum):
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    DECIMAL = "DECIMAL"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    BOOLEAN = "BOOLEAN"
    JSON = "JSON"
    JSONB = "JSONB"
```

---

## Complete Example

```python
import asyncio
from src.migration.orchestrator import MigrationOrchestrator
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType
from src.data_generators.synthetic_data import SyntheticDataGenerator

async def main():
    # Initialize
    orchestrator = MigrationOrchestrator()
    generator = SyntheticDataGenerator(seed=42)
    
    # Create legacy table
    table = DB2Table(
        schema="PROD",
        table_name="CUSTOMERS",
        columns=[
            DB2Column("CUSTOMER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("NAME", DB2DataType.VARCHAR, length=100),
            DB2Column("EMAIL", DB2DataType.VARCHAR, length=100)
        ],
        primary_key=["CUSTOMER_ID"]
    )
    orchestrator.legacy_env.db2.create_table(table)
    
    # Generate and insert data
    customers = generator.generate_db2_customer_data(count=1000)
    orchestrator.legacy_env.db2.insert_data("PROD", "CUSTOMERS", customers)
    
    # Run migration
    result = await orchestrator.run_migration(
        source="db2_legacy",
        target="postgresql_cloud",
        workflow="api_driven",
        migration_plan={
            "estimated_records": 1000,
            "table_count": 1,
            "business_criticality": "HIGH",
            "max_downtime_hours": 4
        }
    )
    
    # Check results
    print(f"Migration Status: {result.status.value}")
    print(f"Records Migrated: {result.records_migrated}")
    print(f"Duration: {result.duration:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Error Handling

All async methods may raise exceptions:

```python
try:
    result = await orchestrator.run_migration(...)
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Migration failed: {e}")
    # Trigger rollback if needed
```

---

## See Also

- [Architecture Blueprint](architecture.md)
- [User Guide](user_guide.md)
- [Technical Documentation](technical_documentation.md)
- [Patent Specification](patent_specification.md)
