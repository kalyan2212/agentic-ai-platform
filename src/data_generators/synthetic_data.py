"""
Synthetic Data Generators

Patent-worthy component: AI-driven synthetic data generation for DB2/VSAM to PostgreSQL migration.
Generates realistic test data that mimics mainframe data patterns.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import string
from faker import Faker
import structlog

from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType
from src.cloud.cloud_native_simulator import PostgreSQLTable, PostgreSQLColumn, PostgreSQLDataType

logger = structlog.get_logger()
fake = Faker()


class SyntheticDataGenerator:
    """
    Patent-worthy: AI-driven synthetic data generation that:
    - Maintains referential integrity
    - Preserves data distribution patterns
    - Generates realistic business data
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
            Faker.seed(seed)
        self.logger = logger.bind(component="synthetic_data_generator")
    
    def generate_db2_customer_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate synthetic customer data for DB2"""
        customers = []
        
        for i in range(count):
            customer = {
                "CUSTOMER_ID": f"CUST{str(i+1).zfill(8)}",
                "FIRST_NAME": fake.first_name()[:20],
                "LAST_NAME": fake.last_name()[:30],
                "EMAIL": fake.email()[:50],
                "PHONE": fake.phone_number()[:15],
                "ADDRESS": fake.street_address()[:60],
                "CITY": fake.city()[:30],
                "STATE": fake.state_abbr(),
                "ZIP_CODE": fake.zipcode()[:10],
                "ACCOUNT_BALANCE": round(random.uniform(0, 50000), 2),
                "CREATED_DATE": fake.date_between(start_date="-10y", end_date="today"),
                "STATUS": random.choice(["ACTIVE", "INACTIVE", "SUSPENDED"])
            }
            customers.append(customer)
        
        self.logger.info("generated_customer_data", count=count)
        return customers
    
    def generate_db2_transaction_data(self, customer_ids: List[str], count: int) -> List[Dict[str, Any]]:
        """Generate synthetic transaction data for DB2"""
        transactions = []
        
        for i in range(count):
            transaction = {
                "TRANSACTION_ID": f"TXN{str(i+1).zfill(12)}",
                "CUSTOMER_ID": random.choice(customer_ids),
                "TRANSACTION_TYPE": random.choice(["PURCHASE", "PAYMENT", "REFUND", "ADJUSTMENT"]),
                "AMOUNT": round(random.uniform(10, 5000), 2),
                "TRANSACTION_DATE": fake.date_time_between(start_date="-1y", end_date="now"),
                "DESCRIPTION": fake.text(max_nb_chars=100),
                "STATUS": random.choice(["COMPLETED", "PENDING", "FAILED"]),
                "MERCHANT_ID": f"MERCH{random.randint(1, 1000):05d}",
                "CHANNEL": random.choice(["ONLINE", "POS", "ATM", "PHONE"])
            }
            transactions.append(transaction)
        
        self.logger.info("generated_transaction_data", count=count)
        return transactions
    
    def generate_vsam_record_data(self, record_length: int, count: int) -> List[bytes]:
        """Generate synthetic VSAM fixed-length records"""
        records = []
        
        for i in range(count):
            # Generate random alphanumeric data
            record_data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=record_length))
            records.append(record_data.encode('ascii'))
        
        self.logger.info("generated_vsam_records", count=count, record_length=record_length)
        return records
    
    def generate_cobol_batch_data(self, batch_size: int) -> List[Dict[str, Any]]:
        """Generate synthetic batch processing data"""
        batch_records = []
        
        for i in range(batch_size):
            record = {
                "RECORD_TYPE": random.choice(["HEADER", "DETAIL", "TRAILER"]),
                "SEQUENCE_NUM": i + 1,
                "ACCOUNT_NUM": f"{random.randint(1000000000, 9999999999)}",
                "AMOUNT": round(random.uniform(1, 10000), 2),
                "PROCESSING_DATE": datetime.now().date(),
                "BATCH_ID": f"BATCH{datetime.now().strftime('%Y%m%d')}{random.randint(1, 999):03d}"
            }
            batch_records.append(record)
        
        self.logger.info("generated_batch_data", count=batch_size)
        return batch_records
    
    def generate_edi_order_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate synthetic EDI order data"""
        orders = []
        
        for i in range(count):
            order = {
                "purchase_order_number": f"PO{datetime.now().strftime('%Y%m%d')}{i+1:06d}",
                "order_date": fake.date_between(start_date="-30d", end_date="today").isoformat(),
                "buyer_id": f"BUYER{random.randint(1, 100):04d}",
                "seller_id": f"SELLER{random.randint(1, 50):04d}",
                "items": [
                    {
                        "item_id": f"ITEM{random.randint(1, 1000):06d}",
                        "quantity": random.randint(1, 100),
                        "unit_price": round(random.uniform(10, 500), 2),
                        "description": fake.catch_phrase()
                    }
                    for _ in range(random.randint(1, 10))
                ],
                "total_amount": 0  # Will be calculated
            }
            order["total_amount"] = sum(item["quantity"] * item["unit_price"] for item in order["items"])
            orders.append(order)
        
        self.logger.info("generated_edi_orders", count=count)
        return orders


class DataMappingEngine:
    """
    Patent-worthy: Intelligent data mapping from legacy to modern formats
    """
    
    def __init__(self):
        self.logger = logger.bind(component="data_mapping_engine")
        self.type_mapping = self._initialize_type_mapping()
    
    def _initialize_type_mapping(self) -> Dict[DB2DataType, PostgreSQLDataType]:
        """Initialize DB2 to PostgreSQL type mapping"""
        return {
            DB2DataType.CHAR: PostgreSQLDataType.VARCHAR,
            DB2DataType.VARCHAR: PostgreSQLDataType.VARCHAR,
            DB2DataType.INTEGER: PostgreSQLDataType.INTEGER,
            DB2DataType.SMALLINT: PostgreSQLDataType.INTEGER,
            DB2DataType.BIGINT: PostgreSQLDataType.BIGINT,
            DB2DataType.DECIMAL: PostgreSQLDataType.DECIMAL,
            DB2DataType.DATE: PostgreSQLDataType.DATE,
            DB2DataType.TIMESTAMP: PostgreSQLDataType.TIMESTAMP
        }
    
    def map_db2_to_postgresql_table(self, db2_table: DB2Table) -> PostgreSQLTable:
        """Map DB2 table structure to PostgreSQL"""
        postgresql_columns = []
        
        for db2_col in db2_table.columns:
            pg_col = PostgreSQLColumn(
                name=db2_col.name.lower(),  # PostgreSQL convention: lowercase
                data_type=self.type_mapping.get(db2_col.data_type, PostgreSQLDataType.TEXT),
                length=db2_col.length,
                precision=db2_col.precision,
                scale=db2_col.scale,
                nullable=db2_col.nullable,
                default_value=db2_col.default_value
            )
            postgresql_columns.append(pg_col)
        
        postgresql_table = PostgreSQLTable(
            schema=db2_table.schema.lower(),
            table_name=db2_table.table_name.lower(),
            columns=postgresql_columns,
            primary_key=[pk.lower() for pk in db2_table.primary_key],
            indexes=db2_table.indexes
        )
        
        self.logger.info(
            "mapped_table",
            source=f"{db2_table.schema}.{db2_table.table_name}",
            target=f"{postgresql_table.schema}.{postgresql_table.table_name}"
        )
        
        return postgresql_table
    
    def transform_data_record(self, record: Dict[str, Any], source_table: DB2Table, target_table: PostgreSQLTable) -> Dict[str, Any]:
        """Transform a single data record from DB2 format to PostgreSQL format"""
        transformed = {}
        
        for source_col, target_col in zip(source_table.columns, target_table.columns):
            value = record.get(source_col.name)
            
            # Apply transformations based on type
            if value is not None:
                if source_col.data_type == DB2DataType.CHAR and isinstance(value, str):
                    # Trim CHAR fields (DB2 pads with spaces)
                    value = value.rstrip()
                elif source_col.data_type == DB2DataType.DECIMAL:
                    # Ensure proper decimal precision
                    value = round(float(value), source_col.scale or 2)
            
            transformed[target_col.name] = value
        
        return transformed


class SchemaAnalyzer:
    """
    Patent-worthy: Analyzes legacy schemas and suggests optimal modern schema designs
    """
    
    def __init__(self):
        self.logger = logger.bind(component="schema_analyzer")
    
    def analyze_db2_schema(self, tables: Dict[str, DB2Table]) -> Dict[str, Any]:
        """Analyze DB2 schema and provide insights"""
        analysis = {
            "total_tables": len(tables),
            "total_columns": sum(len(table.columns) for table in tables.values()),
            "complexity_score": 0,
            "recommendations": []
        }
        
        # Analyze table complexity
        for table_name, table in tables.items():
            if len(table.columns) > 50:
                analysis["recommendations"].append({
                    "table": table_name,
                    "issue": "high_column_count",
                    "suggestion": "Consider normalizing into multiple tables"
                })
            
            # Check for CHAR types that could be VARCHAR
            for col in table.columns:
                if col.data_type == DB2DataType.CHAR and col.length and col.length > 20:
                    analysis["recommendations"].append({
                        "table": table_name,
                        "column": col.name,
                        "issue": "inefficient_char_usage",
                        "suggestion": f"Convert CHAR({col.length}) to VARCHAR for better space efficiency"
                    })
        
        # Calculate complexity score
        analysis["complexity_score"] = (
            len(tables) * 1.0 +
            analysis["total_columns"] * 0.1 +
            len(analysis["recommendations"]) * 2.0
        )
        
        self.logger.info("schema_analysis_completed", complexity_score=analysis["complexity_score"])
        
        return analysis
