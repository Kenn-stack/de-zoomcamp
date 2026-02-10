# 🚕 NYC Taxi Data Warehouse Project

## 📌 Overview

This project builds a **cloud-based data warehouse** using **Google BigQuery** and **Google Cloud Storage (GCS)**.
It ingests raw NYC Taxi trip data from public datasets, stages it as **external tables**, and loads it into **native BigQuery tables** optimized for analytics.

---


## 📂 Project Structure

```
03-data-warehouse/
├── load_yellow_taxi_data.py   # Uploads data to GCS
├── create_external_tables.sql # BigQuery external tables
├── create_native_tables.sql  # BigQuery internal tables
├── pyproject.toml
├── uv.lock
└── README.md
```
---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/data-engineering-zoomcamp.git
cd data-engineering-zoomcamp/03-data-warehouse
```
Change the bucket name and path to service account credentials when it applies.
---

### 2️⃣ Set up Python environment (uv)

Install dependencies:

```bash
uv sync
```

Or add missing ones:

```bash
uv add google-cloud-storage
```
---

### 4️⃣ Upload data to GCS

```bash
uv run python load_yellow_taxi_data.py
```

This uploads NYC Taxi CSV files to your GCS bucket.

