### ADR-003: Message Broker Selection - RabbitMQ over In-Memory Redis

#### Status
**Accepted**

#### Context
We need a message broker to transport job messages between the REST API and background workers. We evaluated Redis (Key-Value/List store) versus RabbitMQ (AMQP Message Broker).

#### Decision
We will use **RabbitMQ (AMQP protocol)** as the primary message broker.

#### Justification
* RabbitMQ provides strict AMQP semantics with explicit separation between *Exchanges* and *Queues*.
* Supports native message durability, persistent queues, and client-level acknowledgment.
* Supports per-channel prefetch limits (`worker_prefetch_multiplier=1`) and queue depth monitoring for auto-scaling.

#### Consequences
* **Positive:**
  * High reliability and zero message loss during worker crashes.
  * Support for Advanced AMQP patterns (Dead Letter Exchanges, Topic Exchanges).
* **Negative:**
  * Requires running a local RabbitMQ AMQP broker (Erlang runtime or service).

#### Compliance
The system configuration (`app/config.py`) MUST default to AMQP protocol URIs (`amqp://guest:guest@localhost:5672//`).

#### Notes
* **Date:** October 2026  
