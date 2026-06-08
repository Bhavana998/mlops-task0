# 🚀 MLOps Task 0 — Production-Ready Rolling Mean Signal Pipeline

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)
![MLOps](https://img.shields.io/badge/MLOps-Batch%20Pipeline-success)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

A production-oriented MLOps batch pipeline that processes OHLCV market data, computes rolling averages, generates trading signals, records operational metrics, and maintains complete execution observability through structured logging.

This project focuses not only on solving the task but also on demonstrating engineering practices commonly expected in real-world ML and MLOps systems.

---

# 🎯 Problem Statement

Given OHLCV market data:

* Calculate a rolling mean on the `close` price
* Generate a binary trading signal
* Measure execution metrics
* Maintain reproducible results
* Produce operational logs
* Support containerized deployment

Signal Logic:

```text
Signal = 1  if close > rolling_mean
Signal = 0  otherwise
```

---

# ✨ Key Features

### Data Processing

* Robust CSV ingestion
* Input validation
* Rolling mean calculation
* Binary signal generation

### Observability

* Structured logging
* Console + file logging
* Execution latency tracking
* Metrics reporting

### Reliability

* Graceful error handling
* Configuration validation
* Missing data checks
* Deterministic execution

### Production Readiness

* Dockerized deployment
* Config-driven execution
* Reproducible outputs
* Clean project structure

---

# 🏗️ System Architecture

```text
                    +----------------+
                    |    data.csv    |
                    +----------------+
                             |
                             v
                 +----------------------+
                 | Data Validation Layer |
                 +----------------------+
                             |
                             v
                 +----------------------+
                 | Rolling Mean Engine  |
                 +----------------------+
                             |
                             v
                 +----------------------+
                 | Signal Generator     |
                 +----------------------+
                             |
          +------------------+------------------+
          |                                     |
          v                                     v
 +--------------------+             +--------------------+
 |    metrics.json    |             |      run.log       |
 +--------------------+             +--------------------+
```

---

# ⚙️ Project Structure

```text
## 📁 Repository Structure

```text
mlops-task-0/
│
├── .dockerignore            # Docker ignore rules
├── Dockerfile               # Container definition
├── Makefile                 # Build and run automation
├── config.yaml              # Pipeline configuration
├── data.csv                 # Input OHLCV dataset
├── metrics.json             # Generated metrics output
├── pyproject.toml           # Project metadata and dependencies
├── requirements.txt         # Python dependencies
├── run.py                   # Main pipeline entry point
├── run.log                  # Execution logs
│
├── load_data/               # Data loading module
│   └── ...
│
└── make/                    # Utility scripts
    └── ...
```

### Directory Overview

| File / Folder      | Purpose                                                        |
| ------------------ | -------------------------------------------------------------- |
| `run.py`           | Executes the complete batch pipeline                           |
| `config.yaml`      | Stores configurable parameters such as rolling window and seed |
| `data.csv`         | Input OHLCV dataset used for signal generation                 |
| `load_data/`       | Handles data ingestion and validation                          |
| `metrics.json`     | Stores pipeline execution metrics                              |
| `run.log`          | Stores structured execution logs                               |
| `Dockerfile`       | Containerizes the application                                  |
| `Makefile`         | Simplifies common commands such as build and run               |
| `requirements.txt` | Python package dependencies                                    |
| `pyproject.toml`   | Python project configuration                                   |
| `.dockerignore`    | Excludes unnecessary files from Docker builds                  |

This structure follows a modular and production-oriented design, separating configuration, execution, logging, data ingestion, and deployment assets for better maintainability and scalability.

```
```

```

---

# 📂 Input Dataset

Expected CSV Format:

```csv
timestamp,open,high,low,close,volume
2024-01-01,100,102,99,101,5000
2024-01-02,101,104,100,103,5200
...
```

Required Column:

```text
close
```

The pipeline validates the presence of required columns before processing.

---

# ⚙️ Configuration

Example `config.yaml`

```yaml
version: v1
seed: 42
window: 5
```

| Parameter | Description              |
| --------- | ------------------------ |
| version   | Pipeline version         |
| seed      | Reproducibility seed     |
| window    | Rolling mean window size |

---

# 🚀 Local Execution

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run Pipeline

```bash
python run.py \
  --input data.csv \
  --config config.yaml \
  --output metrics.json \
  --log-file run.log
```

---

# 🐳 Docker Execution

## Build Image

```bash
docker build -t mlops-task .
```

## Run Container

```bash
docker run --rm mlops-task
```

The container executes the pipeline and generates:

```text
metrics.json
run.log
```

---

# 📊 Example Output

Generated `metrics.json`

```json
{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 45,
  "seed": 42,
  "status": "success"
}
```

---

# 📈 Metrics Explained

| Metric         | Description                    |
| -------------- | ------------------------------ |
| rows_processed | Number of valid rows processed |
| signal_rate    | Percentage of positive signals |
| latency_ms     | Total execution latency        |
| seed           | Reproducibility seed           |
| status         | Pipeline execution status      |
| version        | Release version                |

---

# 🔍 Signal Generation Process

Example:

```text
Close Prices

[100, 102, 104, 105, 107]
```

Rolling Mean (window=5)

```text
[NaN, NaN, NaN, NaN, 103.6]
```

Generated Signal

```text
107 > 103.6

Signal = 1
```

The first `window - 1` rows are excluded because the rolling mean cannot be computed for them.

For a dataset with:

```text
10000 rows
window = 5
```

Valid rows:

```text
10000 - 4 = 9996
```

---

# 🧠 Engineering Decisions

## Why Rolling Mean?

Rolling averages are widely used in quantitative finance to smooth noisy price movements and identify underlying trends.

---

## Why Config-Driven Design?

Separating configuration from code enables:

* Easier experimentation
* Better maintainability
* Environment portability
* Cleaner deployments

---

## Why Docker?

Docker ensures:

* Environment consistency
* Dependency isolation
* Reproducible execution
* Deployment portability

---

## Why Logging?

Production systems require visibility.

Logs provide:

* Debugging support
* Monitoring capability
* Failure diagnosis
* Operational auditing

---

# 🛡️ Error Handling Strategy

The pipeline gracefully handles:

### Missing Input File

```json
{
  "status": "error",
  "error_message": "Input file not found"
}
```

### Missing Close Column

```json
{
  "status": "error",
  "error_message": "Column 'close' not found"
}
```

### Empty Dataset

```json
{
  "status": "error",
  "error_message": "Dataset is empty"
}
```

### Invalid Configuration

```json
{
  "status": "error",
  "error_message": "Invalid configuration"
}
```

No unhandled exceptions are exposed to end users.

---

# 📜 Logging Strategy

Every execution step is logged.

Example:

```text
2026-06-08 10:00:00 INFO Pipeline started
2026-06-08 10:00:00 INFO Configuration loaded
2026-06-08 10:00:01 INFO Rows processed: 9996
2026-06-08 10:00:01 INFO Signal rate: 0.4991
2026-06-08 10:00:01 INFO Pipeline completed
```

Logs are written to:

```text
run.log
stdout
```

---

# 🔄 Reproducibility

The pipeline guarantees deterministic execution through:

* Fixed random seed
* Configuration-driven behavior
* Dockerized environment
* Consistent data processing logic

Running the pipeline multiple times on the same dataset produces identical results.

---

# 🧪 Validation Checklist

* [x] CSV validation
* [x] Configuration validation
* [x] Deterministic execution
* [x] Logging enabled
* [x] Metrics generated
* [x] Docker support
* [x] Error handling implemented
* [x] Production-ready structure

---

# 🔮 Future Improvements

Potential enterprise-scale enhancements:

* GitHub Actions CI/CD
* PyTest Unit Testing
* MLflow Experiment Tracking
* Airflow Orchestration
* Kubernetes Deployment
* Prometheus Monitoring
* Grafana Dashboards
* Data Drift Detection
* Feature Store Integration
* Cloud Deployment (AWS/GCP/Azure)

---

# 💼 What This Project Demonstrates

This repository showcases engineering practices expected from modern MLOps and Machine Learning Engineers:

✅ Data Validation

✅ Reproducibility

✅ Configuration Management

✅ Structured Logging

✅ Metrics Tracking

✅ Error Handling

✅ Dockerization

✅ Observability

✅ Production Mindset

While the business logic is intentionally simple, the architecture reflects how real-world ML systems are designed, monitored, and deployed.

---

# 👩‍💻 Author

**Bhavana Setty**

Aspiring AI/ML & MLOps Engineer

GitHub: https://github.com/Bhavana998

---

# 📄 License

MIT License

Copyright (c) 2026 Bhavana Setty
