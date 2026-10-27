
### ADR-001: Adoption of Event-Driven Architecture (Broker Topology)

#### Status
**Accepted**

#### Context
Long-running background tasks (PDF generation, email delivery, heavy data processing) invoked synchronously during HTTP requests cause high response latencies (>3000ms), HTTP gateway timeouts, and UI thread exhaustion. We need an architectural style that maximizes system responsiveness and handles load spikes cleanly.

#### Decision
We will adopt an **Event-Driven Architecture (EDA)** utilizing the **Broker Topology**. 
The API server acts as an Event Producer, publishing job execution events to a central message broker. Independent Celery worker processes act as Event Processors, asynchronously consuming tasks from the broker (*Competing Consumers pattern*).

#### Consequences
* **Positive:**
  * System responsiveness improves from ~3100ms to <25ms for API consumers.
  * Provides a *Backpressure Point*: high message volume is safely buffered in broker queues without crashing the API.
  * Fine-grained horizontal scaling: worker processes can scale independently based on queue depth.
* **Negative:**
  * Introduces asynchronous complexity and eventual consistency.
  * Requires explicit polling (`GET /api/v1/jobs/{job_id}`) or WebSocket connections for status retrieval.

#### Compliance
Automated integration tests MUST verify that `POST /api/v1/jobs` returns `HTTP 202 Accepted` within 50ms without executing task logic inline during production runs.

#### Notes
* **Date:** October 2026  