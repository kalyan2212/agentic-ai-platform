"""
FastAPI application for B2B Customer Migration Platform
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

from src.models.customer import Customer, IntegrationChannel
from src.orchestration.migration_orchestrator import MigrationOrchestrator
from src.risk.risk_assessor import RiskAssessor
from src.simulation.simulation_engine import SimulationEngine

app = FastAPI(
    title="B2B Customer Migration Platform",
    description="Intelligent platform for migrating B2B customers from legacy to modern cloud-native applications",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
orchestrator = MigrationOrchestrator()
risk_assessor = RiskAssessor()
simulation_engine = SimulationEngine()

# In-memory storage (in production, use a database)
customers_db = {}


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "B2B Customer Migration Platform API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Customer Management Endpoints

@app.post("/api/customers", response_model=Customer)
def create_customer(customer: Customer):
    """Create a new customer"""
    if customer.customer_id in customers_db:
        raise HTTPException(status_code=400, detail="Customer already exists")
    
    customers_db[customer.customer_id] = customer
    return customer


@app.get("/api/customers", response_model=List[Customer])
def list_customers():
    """List all customers"""
    return list(customers_db.values())


@app.get("/api/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: str):
    """Get a specific customer"""
    customer = customers_db.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.put("/api/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: str, customer: Customer):
    """Update a customer"""
    if customer_id not in customers_db:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer.customer_id = customer_id
    customers_db[customer_id] = customer
    return customer


# Risk Assessment Endpoints

@app.post("/api/risk-assessment/customer/{customer_id}")
def assess_customer_risk(customer_id: str):
    """Perform risk assessment for a customer"""
    customer = customers_db.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    assessment = risk_assessor.assess_customer(customer)
    return assessment.model_dump()


@app.post("/api/risk-assessment/channel/{customer_id}/{channel_id}")
def assess_channel_risk(customer_id: str, channel_id: str):
    """Perform risk assessment for a specific channel"""
    customer = customers_db.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    channel = next((ch for ch in customer.channels if ch.channel_id == channel_id), None)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    
    assessment = risk_assessor.assess_channel(customer, channel)
    return assessment.model_dump()


# Migration Planning Endpoints

@app.post("/api/migrations/plan")
def create_migration_plan(customer_id: str, strategy: str = "phased"):
    """Create a migration plan for a customer"""
    customer = customers_db.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    plan = orchestrator.create_migration_plan(customer, strategy)
    return plan.model_dump()


@app.get("/api/migrations/{plan_id}")
def get_migration_plan(plan_id: str):
    """Get migration plan details"""
    plan = orchestrator.migration_plans.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Migration plan not found")
    
    return plan.model_dump()


@app.get("/api/migrations/{plan_id}/status")
def get_migration_status(plan_id: str):
    """Get migration status"""
    try:
        status = orchestrator.get_migration_status(plan_id)
        return status
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Simulation Endpoints

@app.post("/api/simulations/run/{plan_id}")
def run_simulations(plan_id: str):
    """Run simulations for a migration plan"""
    try:
        results = orchestrator.run_simulations(plan_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Migration Execution Endpoints

@app.post("/api/migrations/{plan_id}/execute")
def execute_migration(plan_id: str, channel_id: Optional[str] = None):
    """Execute migration"""
    try:
        plan = orchestrator.execute_migration(plan_id, channel_id)
        return plan.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/migrations/{plan_id}/rollback")
def rollback_migration(plan_id: str, channel_id: Optional[str] = None, reason: str = "Manual rollback"):
    """Rollback migration"""
    try:
        plan = orchestrator.rollback_migration(plan_id, channel_id, reason)
        return plan.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Analytics and Reporting Endpoints

@app.get("/api/analytics/overview")
def get_analytics_overview():
    """Get migration analytics overview"""
    total_customers = len(customers_db)
    total_plans = len(orchestrator.migration_plans)
    
    completed_migrations = sum(
        1 for plan in orchestrator.migration_plans.values()
        if plan.overall_status.value == "completed"
    )
    
    in_progress_migrations = sum(
        1 for plan in orchestrator.migration_plans.values()
        if plan.overall_status.value == "in_progress"
    )
    
    return {
        "total_customers": total_customers,
        "total_migration_plans": total_plans,
        "completed_migrations": completed_migrations,
        "in_progress_migrations": in_progress_migrations,
        "success_rate": (completed_migrations / total_plans * 100) if total_plans > 0 else 0
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
