# Performance Tests

This project implements performance tests for
the [Performance QA Engineer Course](https://github.com/Nikita-Filonov/performance-qa-engineer-course) stand — a
full-featured educational banking system designed for testing and performance validation in training environments. The
platform includes services such as `Kafka`, `Redis`, `PostgreSQL`, `MinIO`, `Grafana`, `Prometheus` and exposes its API
via both HTTP and gRPC protocols.

**Technologies used**:

- `Python`
- `Locust`
- `Pydantic`
- `gRPC` / `grpcio`
- `HTTP` / `HTTPX`
- `Docker`
- `Kafka`
- `Redis`
- `PostgreSQL`
- `MinIO`
- `Grafana`
- `Prometheus`

Performance tests are written in **Python** using **Locust** and follow modern software engineering principles like
**SOLID**, **DRY**, and **KISS**. They are designed to simulate realistic business flows and provide visibility into
system performance under load.


---

## Table of Contents

- [Project Overview](#project-overview)
- [Best Practices](#best-practices)
- [Getting Started](#getting-started)
- [Running Performance Tests](#running-performance-tests)
- [Monitoring & Observability](#monitoring--observability)
- [CI/CD](#cicd)

---

## Project Overview

This performance testing framework supports both **HTTP** and **gRPC** APIs using a unified test structure.

Key components:

- **Scenarios**: Represent realistic user flows, implemented via Locust user classes.
- **API Clients**: Custom reusable HTTP/gRPC clients located in [clients/http/](./clients/http)
  and [clients/grpc/](./clients/grpc), independent of Locust internals.
- **Seeding**: Automated test data generation via a flexible [seeding builder](./seeds/builder.py), triggered through
  Locust event hooks based on the active [scenario plan](./seeds/schema/plan.py).
- **Tools**: Includes generators for fake data, base configurations, and shared Locust user logic.
- **Reporting**: Built-in HTML reports for Locust runs; Prometheus and Grafana metrics available via the course test
  stand.

Supported business scenarios include:

- Existing user: make purchase, get documents, issue virtual card, view operations
- New user: create account, top up card, issue physical card, retrieve account list and documents

---

## Best Practices

This project follows industry-standard best practices:

- **SOLID** design principles for maintainable client architecture
- **DRY** approach to avoid duplication across protocols
- **KISS** philosophy to keep scenarios readable and focused
- Flexible structure to support both HTTP and gRPC testing
- Reusable API clients, designed to be composable and injectable
- The framework is easy to extend with new scenarios or client implementations as the system evolves

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/natalysoliton/performance-tests.git
cd performance-tests
```

### 2. Create a Virtual Environment

#### Linux / MacOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running Performance Tests

Each scenario can be launched via its own configuration file. The report will be automatically saved in the same
directory.

Example:

```bash
locust --config=./scenarios/http/gateway/existing_user_get_documents/v1.0.conf
```

After test execution, open the generated HTML report: `./scenarios/http/gateway/existing_user_get_documents/report.html`

---

## Monitoring & Observability

In addition to built-in Locust reports, system-level metrics can be explored via:

- **Grafana:** http://localhost:3002
- **Prometheus:** http://localhost:9090

These dashboards are preconfigured in
the [course infrastructure repository](https://github.com/Nikita-Filonov/performance-qa-engineer-course).

---

## CI/CD

GitHub Actions integration is enabled for this project. You can execute scenarios in headless mode and publish reports
to GitHub Pages automatically.

Configuration can be found in [.github/workflows/performance-tests.yml](./.github/workflows/performance-tests.yml).