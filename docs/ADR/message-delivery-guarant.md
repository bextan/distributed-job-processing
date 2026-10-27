### ADR-004: Guaranteed Message Delivery via Late Acknowledgment (`task_acks_late`)

#### Status
**Accepted**

#### Context
In standard messaging, if a worker process dequeues a message and immediately acknowledges it, a worker crash causes permanent task loss before execution completes.

#### Decision
We will configure Celery workers with **`task_acks_late = True`** and **`worker_prefetch_multiplier = 1`**.

#### Consequences
* **Positive:**
  * Guarantees *At-Least-Once Delivery*. If a worker process terminates mid-execution, RabbitMQ automatically re-queues the unacknowledged message and delivers it to another worker.
  * Prevents worker starvation and unfair task distribution.
* **Negative:**
  * Tasks MUST be written idempotently, as re-delivered tasks after worker crashes may execute again from the start.

#### Compliance
All Celery tasks defined in `app/workers/tasks.py` MUST be idempotent or utilize idempotency keys.

#### Notes
* **Date:** October 2026  