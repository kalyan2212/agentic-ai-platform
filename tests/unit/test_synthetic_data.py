"""
Unit tests for synthetic data generator
"""

import pytest

from src.data_generators.synthetic_data import (
    SyntheticDataGenerator,
    DataMappingEngine,
    SchemaAnalyzer
)
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType


def test_synthetic_customer_data_generation():
    """Test generating synthetic customer data"""
    generator = SyntheticDataGenerator(seed=42)
    
    customers = generator.generate_db2_customer_data(count=10)
    
    assert len(customers) == 10
    assert all("CUSTOMER_ID" in c for c in customers)
    assert all("EMAIL" in c for c in customers)
    assert all("ACCOUNT_BALANCE" in c for c in customers)


def test_synthetic_transaction_data_generation():
    """Test generating synthetic transaction data"""
    generator = SyntheticDataGenerator(seed=42)
    
    customer_ids = ["CUST001", "CUST002", "CUST003"]
    transactions = generator.generate_db2_transaction_data(customer_ids, count=20)
    
    assert len(transactions) == 20
    assert all("TRANSACTION_ID" in t for t in transactions)
    assert all(t["CUSTOMER_ID"] in customer_ids for t in transactions)


def test_vsam_record_generation():
    """Test generating VSAM records"""
    generator = SyntheticDataGenerator(seed=42)
    
    records = generator.generate_vsam_record_data(record_length=100, count=5)
    
    assert len(records) == 5
    assert all(len(r) == 100 for r in records)
    assert all(isinstance(r, bytes) for r in records)


def test_cobol_batch_data_generation():
    """Test generating COBOL batch data"""
    generator = SyntheticDataGenerator(seed=42)
    
    batch_data = generator.generate_cobol_batch_data(batch_size=15)
    
    assert len(batch_data) == 15
    assert all("RECORD_TYPE" in r for r in batch_data)
    assert all("BATCH_ID" in r for r in batch_data)


def test_edi_order_data_generation():
    """Test generating EDI order data"""
    generator = SyntheticDataGenerator(seed=42)
    
    orders = generator.generate_edi_order_data(count=5)
    
    assert len(orders) == 5
    assert all("purchase_order_number" in o for o in orders)
    assert all("items" in o for o in orders)
    assert all(len(o["items"]) > 0 for o in orders)


def test_db2_to_postgresql_type_mapping():
    """Test DB2 to PostgreSQL data type mapping"""
    mapper = DataMappingEngine()
    
    assert DB2DataType.VARCHAR in mapper.type_mapping
    assert DB2DataType.INTEGER in mapper.type_mapping
    assert DB2DataType.DECIMAL in mapper.type_mapping


def test_table_mapping():
    """Test mapping DB2 table to PostgreSQL"""
    mapper = DataMappingEngine()
    
    db2_table = DB2Table(
        schema="LEGACY",
        table_name="CUSTOMERS",
        columns=[
            DB2Column("CUSTOMER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("NAME", DB2DataType.VARCHAR, length=50),
            DB2Column("BALANCE", DB2DataType.DECIMAL, precision=10, scale=2)
        ],
        primary_key=["CUSTOMER_ID"]
    )
    
    pg_table = mapper.map_db2_to_postgresql_table(db2_table)
    
    assert pg_table.schema == "legacy"  # Lowercase
    assert pg_table.table_name == "customers"  # Lowercase
    assert len(pg_table.columns) == 3
    assert pg_table.primary_key == ["customer_id"]  # Lowercase


def test_data_record_transformation():
    """Test transforming data record from DB2 to PostgreSQL format"""
    mapper = DataMappingEngine()
    
    db2_table = DB2Table(
        schema="TEST",
        table_name="DATA",
        columns=[
            DB2Column("ID", DB2DataType.INTEGER),
            DB2Column("NAME", DB2DataType.CHAR, length=20)
        ]
    )
    
    pg_table = mapper.map_db2_to_postgresql_table(db2_table)
    
    db2_record = {
        "ID": 123,
        "NAME": "Test Name       "  # CHAR field padded with spaces
    }
    
    pg_record = mapper.transform_data_record(db2_record, db2_table, pg_table)
    
    assert pg_record["id"] == 123
    assert pg_record["name"] == "Test Name"  # Spaces trimmed


def test_schema_analyzer():
    """Test schema analysis"""
    analyzer = SchemaAnalyzer()
    
    tables = {
        "TEST.TABLE1": DB2Table(
            schema="TEST",
            table_name="TABLE1",
            columns=[
                DB2Column(f"COL{i}", DB2DataType.VARCHAR, length=50)
                for i in range(60)  # High column count
            ]
        ),
        "TEST.TABLE2": DB2Table(
            schema="TEST",
            table_name="TABLE2",
            columns=[
                DB2Column("ID", DB2DataType.INTEGER),
                DB2Column("NAME", DB2DataType.CHAR, length=100)  # Large CHAR
            ]
        )
    }
    
    analysis = analyzer.analyze_db2_schema(tables)
    
    assert analysis["total_tables"] == 2
    assert analysis["total_columns"] == 62
    assert "recommendations" in analysis
    assert len(analysis["recommendations"]) > 0
    assert "complexity_score" in analysis
