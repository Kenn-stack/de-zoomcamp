# Data Engineering Zoomcamp – Week 2

## Workflow Orchestration with Kestra

This README documents the **Week 2 Workflow Orchestration** module of the Data Engineering Zoomcamp, focusing on **Kestra** as the orchestration engine. It covers core concepts, hands-on workflows, scheduling, backfilling, and common pitfalls encountered during the exercises.

---

## 📌 Overview

Workflow orchestration is a key responsibility of a data engineer. In this module, Kestra is used to:

* Define **declarative data pipelines** using YAML
* Orchestrate **extract, load, and transform** workflows
* Schedule workflows using cron expressions
* Manage retries, failures, and task dependencies
* Work with large datasets (NYC Taxi data)
* Upload to GCS and load to Big Query

Kestra provides:

* Event-driven and scheduled workflows
* Container-native execution
* Built-in plugins for scripts, cloud storage, and databases

---

## 🛠️ Tech Stack

* **Kestra** (Workflow Orchestrator)
* **Docker & Docker Compose**
* **PostgreSQL** (Kestra metadata DB)
* **Shell & Python tasks**
* **NYC Taxi Open Data** (CSV / CSV.GZ files)

---

## 🚀 Getting Started

### 1️⃣ Start Kestra

```bash
docker-compose up -d
```

Once running, access the Kestra UI:

```
http://localhost:8080
```
If prompted for a username and password, use:

```
username: "admin@kestra.io"
password: Admin1234!
```
---

## 📂 Project Structure

```
.
├── docker-compose.yml
├── flows/
│   ├── 01_hello_world.yaml
│   ├── 02_python.yaml
│   └── ...
└── README.md
```

---

## 🧩 Core Concepts

### Flow

A **flow** is a YAML-defined pipeline that contains:

* Triggers
* Tasks
* Dependencies

### Task

A **task** is a single unit of work, such as:

* Running shell commands
* Executing Python scripts
* Downloading files

### Trigger

Triggers define **when** a flow runs:

* Manual
* Scheduled (cron)
* Event-based

---

🔐 Setting Up Secrets in Kestra (Google Credentials)

Many workflows require access to external services such as Google Cloud Storage. Kestra manages sensitive information using Secrets, which are securely stored and injected at runtime.

This setup follows the official Kestra guide for Google credentials.

1️⃣ Create a Google Service Account Key

In Google Cloud Console, create a Service Account

Grant it the required permissions (e.g. Storage Object Viewer / Admin)

Generate a JSON key file

You will obtain a file similar to:

service-account.json
2️⃣ Add the Secret in Kestra

In the Kestra UI:

Navigate to Namespaces → Secrets

Click Create

Set:

Key: GCP_CREDS

Value: Paste the entire contents of the service account JSON file

⚠️ Do not upload the file — paste the JSON text directly.
