### ADR-002: Modular Monolith Topography for the REST API Application

#### Status
**Accepted**

#### Context
Building a microservice network for a single background job platform introduces excessive operational overhead, network latency, and deployment complexity.

#### Decision
We will structure the API application as a **Modular Monolith** using **FastAPI**. 
Domain capabilities (`api/`, `core/`, `models/`, `workers/`) are strictly organized into isolated Python modules within a single codebase, while background worker execution is decoupled into separate processes.

#### Consequences
* **Positive:**
  * Low overall complexity, simplified local setup, and rapid deployment.
  * Clear module boundaries prevent tight coupling between HTTP routing and worker execution logic.
* **Negative:**
  * The API monolith shares a single process space for all endpoints (though background workers run in separate processes).

#### Compliance
Code reviews and linting tools MUST enforce that API endpoint handlers do not import heavy worker execution libraries directly into synchronous request loops.

#### Notes
* **Date:** October 2026  