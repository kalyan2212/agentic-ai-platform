"""
Unit tests for legacy mainframe simulator
"""

import pytest

from src.legacy.mainframe_simulator import (
    DB2Simulator,
    DB2Table,
    DB2Column,
    DB2DataType,
    VSAMSimulator,
    VSAMFile,
    VSAMFileType,
    COBOLSimulator,
    COBOLProgram,
    CICSSimulator,
    CICSProgram,
    CICSTransaction
)


def test_db2_table_creation():
    """Test DB2 table creation"""
    db2 = DB2Simulator()
    
    table = DB2Table(
        schema="TEST",
        table_name="CUSTOMERS",
        columns=[
            DB2Column("ID", DB2DataType.INTEGER),
            DB2Column("NAME", DB2DataType.VARCHAR, length=50)
        ],
        primary_key=["ID"]
    )
    
    db2.create_table(table)
    
    assert "TEST.CUSTOMERS" in db2.tables
    assert "TEST.CUSTOMERS" in db2.data


def test_db2_data_insertion():
    """Test inserting data into DB2 table"""
    db2 = DB2Simulator()
    
    table = DB2Table(
        schema="TEST",
        table_name="USERS",
        columns=[
            DB2Column("USER_ID", DB2DataType.INTEGER),
            DB2Column("USERNAME", DB2DataType.VARCHAR, length=30)
        ]
    )
    
    db2.create_table(table)
    
    records = [
        {"USER_ID": 1, "USERNAME": "alice"},
        {"USER_ID": 2, "USERNAME": "bob"}
    ]
    
    db2.insert_data("TEST", "USERS", records)
    
    assert len(db2.data["TEST.USERS"]) == 2


def test_db2_data_selection():
    """Test selecting data from DB2 table"""
    db2 = DB2Simulator()
    
    table = DB2Table(
        schema="TEST",
        table_name="PRODUCTS",
        columns=[
            DB2Column("PRODUCT_ID", DB2DataType.INTEGER),
            DB2Column("NAME", DB2DataType.VARCHAR, length=50),
            DB2Column("PRICE", DB2DataType.DECIMAL, precision=10, scale=2)
        ]
    )
    
    db2.create_table(table)
    
    records = [
        {"PRODUCT_ID": 1, "NAME": "Widget", "PRICE": 19.99},
        {"PRODUCT_ID": 2, "NAME": "Gadget", "PRICE": 29.99}
    ]
    
    db2.insert_data("TEST", "PRODUCTS", records)
    
    # Select all
    all_data = db2.select_data("TEST", "PRODUCTS")
    assert len(all_data) == 2
    
    # Select with where clause
    filtered = db2.select_data("TEST", "PRODUCTS", {"PRODUCT_ID": 1})
    assert len(filtered) == 1
    assert filtered[0]["NAME"] == "Widget"


def test_vsam_file_creation():
    """Test VSAM file creation"""
    vsam = VSAMSimulator()
    
    vsam_file = VSAMFile(
        file_name="TEST.FILE",
        file_type=VSAMFileType.KSDS,
        record_length=100,
        key_offset=0,
        key_length=10
    )
    
    vsam.create_file(vsam_file)
    
    assert "TEST.FILE" in vsam.files
    assert vsam.files["TEST.FILE"].file_type == VSAMFileType.KSDS


def test_vsam_record_operations():
    """Test VSAM record write and read"""
    vsam = VSAMSimulator()
    
    vsam_file = VSAMFile(
        file_name="DATA.FILE",
        file_type=VSAMFileType.KSDS,
        record_length=50
    )
    
    vsam.create_file(vsam_file)
    
    # Write record
    record = b"A" * 50
    vsam.write_record("DATA.FILE", record)
    
    # Read records
    records = vsam.read_records("DATA.FILE")
    assert len(records) == 1
    assert records[0] == record


def test_vsam_record_length_validation():
    """Test VSAM record length validation"""
    vsam = VSAMSimulator()
    
    vsam_file = VSAMFile(
        file_name="FIXED.FILE",
        file_type=VSAMFileType.KSDS,
        record_length=100
    )
    
    vsam.create_file(vsam_file)
    
    # Try to write wrong length record
    with pytest.raises(ValueError):
        vsam.write_record("FIXED.FILE", b"A" * 50)  # Wrong length


def test_cobol_program_registration():
    """Test COBOL program registration"""
    cobol = COBOLSimulator()
    
    program = COBOLProgram(
        program_name="TESTPROG",
        source_code="IDENTIFICATION DIVISION...",
        input_files=["INPUT.DAT"],
        output_files=["OUTPUT.DAT"]
    )
    
    cobol.register_program(program)
    
    assert "TESTPROG" in cobol.programs


def test_cobol_program_execution():
    """Test COBOL program execution"""
    cobol = COBOLSimulator()
    
    program = COBOLProgram(
        program_name="BATCH001",
        source_code="IDENTIFICATION DIVISION..."
    )
    
    cobol.register_program(program)
    
    result = cobol.execute_program("BATCH001", {"param1": "value1"})
    
    assert result["status"] == "completed"
    assert result["program"] == "BATCH001"
    assert len(cobol.execution_log) == 1


def test_cics_program_registration():
    """Test CICS program registration"""
    cics = CICSSimulator()
    
    program = CICSProgram(
        program_id="PROG001",
        transaction_code="TRN1",
        supported_transactions=[CICSTransaction.INQUIRY, CICSTransaction.UPDATE]
    )
    
    cics.register_program(program)
    
    assert "PROG001" in cics.programs


def test_cics_transaction_execution():
    """Test CICS transaction execution"""
    cics = CICSSimulator()
    
    program = CICSProgram(
        program_id="INQUIRY01",
        transaction_code="INQ1",
        supported_transactions=[CICSTransaction.INQUIRY]
    )
    
    cics.register_program(program)
    
    result = cics.execute_transaction(
        "INQ1",
        CICSTransaction.INQUIRY,
        {"customer_id": "12345"}
    )
    
    assert result["status"] == "completed"
    assert result["transaction_code"] == "INQ1"
    assert len(cics.transaction_log) == 1
