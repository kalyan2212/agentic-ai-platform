# API Reference

## Base URL
```
http://localhost:8000
```

## Authentication
Currently the API uses no authentication for development. In production, implement API key or OAuth 2.0.

---

## Endpoints

### Health & Status

#### GET /
Get API information

**Response:**
```json
{
  "message": "B2B Customer Migration Platform API",
  "version": "1.0.0",
  "documentation": "/docs"
}
```

#### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Customer Management

#### POST /api/customers
Create a new customer

**Request Body:**
```json
{
  "customer_id": "CUST001",
  "name": "Acme Corporation",
  "industry": "Manufacturing",
  "business_criticality": "high",
  "compliance_requirements": ["PCI-DSS", "SOC2"],
  "contact_email": "contact@acme.com",
  "contact_phone": "+1-555-0123",
  "channels": [
    {
      "channel_id": "CH001",
      "channel_type": "edi",
      "name": "EDI Integration",
      "config": {
        "protocol": "X12",
        "version": "4010"
      },
      "transaction_volume": 5000
    }
  ]
}
```

**Response:** 200 OK
```json
{
  "customer_id": "CUST001",
  "name": "Acme Corporation",
  ...
}
```

#### GET /api/customers
List all customers

**Response:** 200 OK
```json
[
  {
    "customer_id": "CUST001",
    "name": "Acme Corporation",
    ...
  }
]
```

#### GET /api/customers/{customer_id}
Get a specific customer

**Parameters:**
- `customer_id` (path): Customer identifier

**Response:** 200 OK
```json
{
  "customer_id": "CUST001",
  "name": "Acme Corporation",
  ...
}
```

#### PUT /api/customers/{customer_id}
Update a customer

**Parameters:**
- `customer_id` (path): Customer identifier

**Request Body:** Same as POST /api/customers

**Response:** 200 OK

---

### Risk Assessment

#### POST /api/risk-assessment/customer/{customer_id}
Perform risk assessment for a customer

**Parameters:**
- `customer_id` (path): Customer identifier

**Response:** 200 OK
```json
{
  "assessment_id": "RISK-abc12345",
  "customer_id": "CUST001",
  "channel_id": null,
  "risk_factors": [
    {
      "factor_id": "BIZ-CRIT-xyz789",
      "category": "business",
      "severity": "high",
      "description": "Business criticality level: high",
      "impact_score": 60.0,
      "likelihood_score": 80.0,
      "mitigation_strategy": "Implement parallel run..."
    }
  ],
  "overall_risk_score": 52.5,
  "risk_level": "high",
  "migration_readiness_score": 47.5,
  "recommended_actions": [
    "Implement phased migration approach...",
    "Conduct thorough simulation testing..."
  ],
  "assessed_at": "2024-01-15T10:30:00Z",
  "assessed_by": "system"
}
```

#### POST /api/risk-assessment/channel/{customer_id}/{channel_id}
Perform risk assessment for a specific channel

**Parameters:**
- `customer_id` (path): Customer identifier
- `channel_id` (path): Channel identifier

**Response:** 200 OK (same structure as customer assessment)

---

### Migration Planning

#### POST /api/migrations/plan
Create a migration plan

**Query Parameters:**
- `customer_id` (required): Customer to migrate
- `strategy` (optional): Migration strategy (phased, big-bang, parallel) - default: phased

**Response:** 200 OK
```json
{
  "plan_id": "PLAN-abc12345",
  "customer_id": "CUST001",
  "customer_name": "Acme Corporation",
  "overall_status": "planning",
  "channel_migrations": [
    {
      "channel_id": "CH001",
      "channel_type": "edi",
      "status": "planning",
      "risk_score": 45.5,
      "playbook_id": "PLAYBOOK-edi",
      "simulation_passed": false,
      "rollback_available": true,
      "cutover_timestamp": null,
      "notes": [
        "Migration playbook: 7 steps",
        "Risk level: medium",
        "Readiness score: 54.5"
      ]
    }
  ],
  "overall_risk_score": 45.5,
  "created_at": "2024-01-15T10:30:00Z",
  "planned_start": "2024-01-22T00:00:00Z",
  "planned_completion": "2024-03-18T00:00:00Z",
  "actual_start": null,
  "actual_completion": null,
  "migration_strategy": "phased"
}
```

#### GET /api/migrations/{plan_id}
Get migration plan details

**Parameters:**
- `plan_id` (path): Migration plan identifier

**Response:** 200 OK (same structure as create plan)

#### GET /api/migrations/{plan_id}/status
Get migration status

**Parameters:**
- `plan_id` (path): Migration plan identifier

**Response:** 200 OK
```json
{
  "plan_id": "PLAN-abc12345",
  "customer_id": "CUST001",
  "customer_name": "Acme Corporation",
  "overall_status": "in_progress",
  "overall_risk_score": 45.5,
  "progress_percentage": 65.0,
  "planned_start": "2024-01-22T00:00:00Z",
  "planned_completion": "2024-03-18T00:00:00Z",
  "actual_start": "2024-01-22T08:00:00Z",
  "actual_completion": null,
  "channels": [
    {
      "channel_id": "CH001",
      "channel_type": "edi",
      "status": "in_progress",
      "risk_score": 45.5,
      "simulation_passed": true,
      "cutover_timestamp": "2024-01-22T10:00:00Z"
    }
  ]
}
```

---

### Simulation

#### POST /api/simulations/run/{plan_id}
Run simulations for a migration plan

**Parameters:**
- `plan_id` (path): Migration plan identifier

**Response:** 200 OK
```json
{
  "CH001": {
    "status": "passed",
    "success_rate": 98.5,
    "details": "All test scenarios passed validation"
  }
}
```

---

### Migration Execution

#### POST /api/migrations/{plan_id}/execute
Execute migration

**Parameters:**
- `plan_id` (path): Migration plan identifier
- `channel_id` (query, optional): Specific channel to migrate

**Response:** 200 OK
```json
{
  "plan_id": "PLAN-abc12345",
  "overall_status": "in_progress",
  ...
}
```

#### POST /api/migrations/{plan_id}/rollback
Rollback migration

**Parameters:**
- `plan_id` (path): Migration plan identifier
- `channel_id` (query, optional): Specific channel to rollback
- `reason` (query, optional): Reason for rollback

**Response:** 200 OK
```json
{
  "plan_id": "PLAN-abc12345",
  "overall_status": "rolled_back",
  ...
}
```

---

### Analytics

#### GET /api/analytics/overview
Get migration analytics overview

**Response:** 200 OK
```json
{
  "total_customers": 50,
  "total_migration_plans": 45,
  "completed_migrations": 38,
  "in_progress_migrations": 5,
  "success_rate": 84.4
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Interactive Documentation

Visit the following URLs when the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Rate Limiting

Currently no rate limiting is implemented. In production, implement appropriate rate limits based on your requirements.

---

## Versioning

API version is included in the response of the root endpoint. Future versions will use URL versioning (e.g., /api/v2/).
