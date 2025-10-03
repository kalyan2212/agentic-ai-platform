"""
Benchmarking Script for Migration Platform

Tests performance and scalability of the migration platform.
"""

import asyncio
import time
from typing import List, Dict, Any

from src.migration.orchestrator import MigrationOrchestrator
from src.legacy.mainframe_simulator import DB2Table, DB2Column, DB2DataType
from src.data_generators.synthetic_data import SyntheticDataGenerator


class MigrationBenchmark:
    """Benchmark suite for migration platform"""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
    
    async def benchmark_small_migration(self) -> Dict[str, Any]:
        """Benchmark small dataset migration (1K records)"""
        print("Running: Small Migration Benchmark (1K records)")
        return await self._run_benchmark("small", record_count=1000, table_count=2)
    
    async def benchmark_medium_migration(self) -> Dict[str, Any]:
        """Benchmark medium dataset migration (10K records)"""
        print("Running: Medium Migration Benchmark (10K records)")
        return await self._run_benchmark("medium", record_count=10000, table_count=5)
    
    async def benchmark_large_migration(self) -> Dict[str, Any]:
        """Benchmark large dataset migration (100K records)"""
        print("Running: Large Migration Benchmark (100K records)")
        return await self._run_benchmark("large", record_count=100000, table_count=10)
    
    async def benchmark_complex_schema(self) -> Dict[str, Any]:
        """Benchmark complex schema migration (50 tables)"""
        print("Running: Complex Schema Benchmark (50 tables)")
        return await self._run_benchmark("complex", record_count=5000, table_count=50)
    
    async def _run_benchmark(self, name: str, record_count: int, table_count: int) -> Dict[str, Any]:
        """Run a benchmark scenario"""
        orchestrator = MigrationOrchestrator()
        data_generator = SyntheticDataGenerator(seed=42)
        
        # Setup phase
        setup_start = time.time()
        
        for i in range(table_count):
            table = DB2Table(
                schema="BENCH",
                table_name=f"TABLE_{i:03d}",
                columns=[
                    DB2Column("ID", DB2DataType.INTEGER),
                    DB2Column("DATA1", DB2DataType.VARCHAR, length=50),
                    DB2Column("DATA2", DB2DataType.VARCHAR, length=100),
                    DB2Column("AMOUNT", DB2DataType.DECIMAL, precision=10, scale=2),
                    DB2Column("TIMESTAMP", DB2DataType.TIMESTAMP)
                ],
                primary_key=["ID"]
            )
            orchestrator.legacy_env.db2.create_table(table)
            
            # Generate data for this table
            records_per_table = record_count // table_count
            records = []
            for j in range(records_per_table):
                records.append({
                    "ID": i * records_per_table + j,
                    "DATA1": f"Data_{i}_{j}",
                    "DATA2": f"LongerData_{i}_{j}_{'x' * 50}",
                    "AMOUNT": (i + j) * 1.5,
                    "TIMESTAMP": "2024-01-01 12:00:00"
                })
            
            orchestrator.legacy_env.db2.insert_data("BENCH", f"TABLE_{i:03d}", records)
        
        setup_time = time.time() - setup_start
        
        # Migration phase
        migration_start = time.time()
        
        migration_plan = {
            "estimated_records": record_count,
            "table_count": table_count,
            "business_criticality": "MEDIUM",
            "max_downtime_hours": 8
        }
        
        result = await orchestrator.run_migration(
            source="db2_legacy",
            target="postgresql_cloud",
            workflow="batch",
            migration_plan=migration_plan
        )
        
        migration_time = time.time() - migration_start
        
        # Calculate metrics
        throughput = result.records_migrated / migration_time if migration_time > 0 else 0
        
        benchmark_result = {
            "name": name,
            "record_count": record_count,
            "table_count": table_count,
            "setup_time": setup_time,
            "migration_time": migration_time,
            "total_time": setup_time + migration_time,
            "records_migrated": result.records_migrated,
            "throughput": throughput,
            "status": result.status.value,
            "phases": len(result.phases)
        }
        
        self.results.append(benchmark_result)
        
        print(f"  Setup time: {setup_time:.3f}s")
        print(f"  Migration time: {migration_time:.3f}s")
        print(f"  Total time: {benchmark_result['total_time']:.3f}s")
        print(f"  Records migrated: {result.records_migrated}")
        print(f"  Throughput: {throughput:.0f} records/second")
        print()
        
        return benchmark_result
    
    async def benchmark_agent_scalability(self) -> Dict[str, Any]:
        """Benchmark agent scalability with varying agent counts"""
        print("Running: Agent Scalability Benchmark")
        
        from src.agents.orchestration import OrchestrationEngine, BaseAgent, AgentRole
        
        results = []
        
        for agent_count in [1, 5, 10, 20]:
            engine = OrchestrationEngine()
            
            # Register agents
            for i in range(agent_count):
                agent = BaseAgent(
                    f"worker_{i}",
                    AgentRole.DATA_MIGRATOR,
                    ["migrate"]
                )
                engine.register_agent(agent)
            
            # Simulate message routing
            from src.agents.orchestration import AgentMessage
            
            start = time.time()
            
            for i in range(1000):
                message = AgentMessage(
                    sender="coordinator",
                    receiver="any",
                    message_type="migrate",
                    content={"data": i}
                )
                await engine.route_message(message)
            
            elapsed = time.time() - start
            throughput = 1000 / elapsed
            
            results.append({
                "agent_count": agent_count,
                "messages": 1000,
                "time": elapsed,
                "throughput": throughput
            })
            
            print(f"  {agent_count} agents: {throughput:.0f} messages/second")
        
        print()
        return {"scalability_results": results}
    
    def print_summary(self):
        """Print benchmark summary"""
        print("=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)
        print()
        
        print(f"{'Benchmark':<20} {'Records':<12} {'Tables':<8} {'Time (s)':<12} {'Throughput':<15}")
        print("-" * 80)
        
        for result in self.results:
            print(f"{result['name']:<20} {result['record_count']:<12} {result['table_count']:<8} "
                  f"{result['total_time']:<12.3f} {result['throughput']:<15.0f}")
        
        print()
        print("=" * 80)


async def run_all_benchmarks():
    """Run complete benchmark suite"""
    print("=" * 80)
    print("MIGRATION PLATFORM BENCHMARKING SUITE")
    print("=" * 80)
    print()
    
    benchmark = MigrationBenchmark()
    
    # Run benchmarks
    await benchmark.benchmark_small_migration()
    await benchmark.benchmark_medium_migration()
    await benchmark.benchmark_large_migration()
    await benchmark.benchmark_complex_schema()
    await benchmark.benchmark_agent_scalability()
    
    # Print summary
    benchmark.print_summary()
    
    print("\nBenchmarking completed!")


if __name__ == "__main__":
    asyncio.run(run_all_benchmarks())
