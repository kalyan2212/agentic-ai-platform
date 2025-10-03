"""
Example: EDI Migration Workflow

Demonstrates migrating EDI/B2B data from mainframe to cloud-native EDI system.
"""

import asyncio
from datetime import datetime

from src.migration.orchestrator import MigrationOrchestrator
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType
from src.cloud.cloud_native_simulator import EDIMessage, EDIMessageType
from src.data_generators.synthetic_data import SyntheticDataGenerator


async def run_edi_migration_example():
    """Run an EDI-specific migration simulation"""
    
    print("=" * 80)
    print("EDI Migration Workflow - B2B Integration Example")
    print("=" * 80)
    print()
    
    # Initialize components
    orchestrator = MigrationOrchestrator()
    data_generator = SyntheticDataGenerator(seed=100)
    
    print("Step 1: Setting up legacy EDI data in DB2...")
    print("-" * 80)
    
    # Create EDI orders table in DB2
    edi_orders_table = DB2Table(
        schema="EDI",
        table_name="ORDERS_850",
        columns=[
            DB2Column("ORDER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("PO_NUMBER", DB2DataType.VARCHAR, length=30),
            DB2Column("BUYER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("SELLER_ID", DB2DataType.VARCHAR, length=20),
            DB2Column("ORDER_DATE", DB2DataType.DATE),
            DB2Column("TOTAL_AMOUNT", DB2DataType.DECIMAL, precision=15, scale=2),
            DB2Column("STATUS", DB2DataType.VARCHAR, length=20)
        ],
        primary_key=["ORDER_ID"]
    )
    
    orchestrator.legacy_env.db2.create_table(edi_orders_table)
    print(f"Created DB2 EDI table: {edi_orders_table.schema}.{edi_orders_table.table_name}")
    print()
    
    print("Step 2: Generating EDI order data...")
    print("-" * 80)
    
    # Generate EDI orders
    edi_orders = data_generator.generate_edi_order_data(count=100)
    
    # Convert to DB2 format
    db2_orders = []
    for order in edi_orders:
        db2_order = {
            "ORDER_ID": f"EDI{order['purchase_order_number'][-10:]}",
            "PO_NUMBER": order['purchase_order_number'],
            "BUYER_ID": order['buyer_id'],
            "SELLER_ID": order['seller_id'],
            "ORDER_DATE": datetime.fromisoformat(order['order_date']),
            "TOTAL_AMOUNT": order['total_amount'],
            "STATUS": "PENDING"
        }
        db2_orders.append(db2_order)
    
    orchestrator.legacy_env.db2.insert_data("EDI", "ORDERS_850", db2_orders)
    print(f"Generated {len(db2_orders)} EDI orders in legacy system")
    print()
    
    print("Step 3: Configuring cloud EDI integration...")
    print("-" * 80)
    
    # The cloud environment already has EDI simulator
    edi_simulator = orchestrator.cloud_env.edi
    print(f"Cloud EDI system ready")
    print()
    
    print("Step 4: Running EDI migration...")
    print("-" * 80)
    
    migration_plan = {
        "source_system": "DB2 EDI Tables",
        "target_system": "Cloud EDI/B2B Integration",
        "estimated_records": len(db2_orders),
        "table_count": 1,
        "business_criticality": "HIGH",
        "max_downtime_hours": 1
    }
    
    # Run migration with EDI workflow
    result = await orchestrator.run_migration(
        source="db2_edi",
        target="cloud_edi",
        workflow="edi",
        migration_plan=migration_plan
    )
    
    print(f"\nMigration Status: {result.status.value}")
    print(f"Records Migrated: {result.records_migrated}")
    print(f"Duration: {result.duration:.2f} seconds")
    print()
    
    print("Step 5: Transforming migrated data to EDI messages...")
    print("-" * 80)
    
    # Get migrated data from PostgreSQL
    migrated_orders = orchestrator.cloud_env.postgresql.select_data("edi", "orders_850")
    
    # Transform to EDI 850 messages
    edi_messages_sent = 0
    for order in migrated_orders[:5]:  # Show first 5
        edi_message = EDIMessage(
            message_type=EDIMessageType.ORDERS,
            sender_id=order.get("buyer_id", "BUYER000"),
            receiver_id=order.get("seller_id", "SELLER000"),
            control_number=order.get("po_number", "PO000"),
            data={
                "order_id": order.get("order_id"),
                "po_number": order.get("po_number"),
                "order_date": str(order.get("order_date")),
                "total_amount": float(order.get("total_amount", 0))
            }
        )
        
        edi_simulator.send_message(edi_message)
        edi_messages_sent += 1
        
        print(f"  EDI 850 Message: {edi_message.control_number}")
        print(f"    Sender: {edi_message.sender_id} → Receiver: {edi_message.receiver_id}")
        print(f"    Amount: ${edi_message.data['total_amount']:.2f}")
    
    print(f"\nTotal EDI messages created: {edi_messages_sent}")
    print()
    
    print("Step 6: EDI Message Queue Status...")
    print("-" * 80)
    
    pending_messages = edi_simulator.get_pending_messages()
    print(f"Pending EDI messages in queue: {len(pending_messages)}")
    
    # Simulate receiving a message
    if pending_messages:
        first_message = pending_messages[0]
        received = edi_simulator.receive_message(first_message.control_number)
        print(f"Sample message received: {received.control_number}")
        print(f"  Type: EDI {received.message_type.value}")
        print(f"  Data: {received.data}")
    
    print()
    
    print("=" * 80)
    print("EDI Migration Completed Successfully!")
    print("=" * 80)
    print()
    print("Summary:")
    print(f"  - Legacy EDI orders migrated: {result.records_migrated}")
    print(f"  - EDI 850 messages generated: {edi_messages_sent}")
    print(f"  - Messages in queue: {len(edi_simulator.get_pending_messages())}")
    print(f"  - Migration duration: {result.duration:.2f} seconds")
    
    return result


if __name__ == "__main__":
    result = asyncio.run(run_edi_migration_example())
