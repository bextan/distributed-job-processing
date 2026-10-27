# Distributed Job Processing Platform (RabbitMQ Broker Version)

A production-grade, modular monolith backend platform that accepts jobs via a REST API, queues them in RabbitMQ (AMQP), processes them asynchronously using Celery workers, and provides real-time job status tracking.

Designed for learning modern backend engineering, asynchronous architectures, and analyzing bottlenecks, trade-offs, reliability, and fault tolerance.

---

## System Architecture

```text
                                  +-----------------------+
                                  |   REST Client / UI    |
                                  +-----------+-----------+
                                              |
                                              | HTTP POST /jobs (Payload)
                                              v
                                  +-----------+-----------+
                                  |   FastAPI Monolith    |
                                  |     (Producer)        |
                                  +-----------+-----------+
                                              |
                                              | Publish AMQP Message
                                              v
                                  +-----------+-----------+
                                  |   RabbitMQ Broker     |
                                  | (Queue: celery / RPC) |
                                  +-----------+-----------+
                                              |
                        +---------------------+---------------------+
                        | AMQP Prefetch (q=1)                       | AMQP Prefetch (q=1)
                        v                                           v
            +-----------+-----------+                   +-----------+-----------+
            | Celery Worker Node 1  |                   | Celery Worker Node 2  |
            +-----------------------+                   +-----------------------+
```

---

## Architectural Comparison: RabbitMQ vs Redis

| Characteristic | RabbitMQ (AMQP) | Redis |
| :--- | :--- | :--- |
| **Primary Design Target** | Enterprise Message Broker (Queueing, Routing, Exchanges) | In-Memory Key-Value Store & Data Grid |
| **Routing Flexibility** | **High:** Supports Direct, Fanout, Topic, and Headers exchanges | **Basic:** Simple point-to-point lists or pub/sub topics |
| **Delivery Guarantees** | Publisher confirms, consumer acknowledgments, persistent queues | Queue item loss possible if Redis crashes before AOF write |
| **Concurrency & Prefetch** | Per-consumer channel prefetch limit (`worker_prefetch_multiplier`) | Redis List polling (`BRPOP`) |
| **Result Backend Support** | Uses `rpc://` (ephemeral reply queues) or external DB | Uses Redis Key-Value Store natively |
| **Use Case Fit** | Complex workflows, strict delivery guarantees, heavy queuing | Ultra-low latency caching, fast prototyping, simple queues |

---

## Local Setup on Windows (Without Docker)

### Prerequisites

1. **Install Erlang & RabbitMQ Server:**
   * Download and install Erlang/OTP and RabbitMQ Server for Windows.
   * Or if using WSL (Windows Subsystem for Linux):
     ```bash
     sudo apt update && sudo apt install -y rabbitmq-server
     sudo service rabbitmq-server start
     ```

2. **Verify RabbitMQ is Running:**
   ```powershell
   # On Windows PowerShell:
   rabbitmqctl status
   
   # Or on WSL:
   wsl sudo rabbitmqctl status
   ```

---

## Running the Application

### 1. Virtual Environment & Dependencies
```powershell
# Navigate to project directory
cd distributed_job_processing_platform_rabbitmq

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Celery Worker (Terminal 1)
```powershell
python run_worker.py
```
*(On Windows, `run_worker.py` automatically sets `--pool=solo` to prevent multiprocessing spawn errors).*

### 3. Start FastAPI REST API Server (Terminal 2)
```powershell
python run_api.py
```
The API server will launch at `http://localhost:8000`.

---

## Running Tests (Terminal 3)

Open a new terminal window to execute automated tests:

```powershell
.\venv\Scripts\activate
pytest tests/
```
*(Tests run in Celery eager mode synchronously without requiring a live RabbitMQ server).*

---

## API Endpoints Summary

* `GET /api/v1/health` — System status and RabbitMQ broker ping.
* `POST /api/v1/jobs` — Enqueue a new asynchronous job (Returns `HTTP 202 Accepted` with `job_id`).
* `GET /api/v1/jobs/{job_id}` — Query job status and result.
* `DELETE /api/v1/jobs/{job_id}` — Revoke/cancel an in-flight job.
