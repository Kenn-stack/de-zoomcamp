
# Docker & SQL

**Description:**
This project ingests and processes data using Python and `uv`. The project is containerized using Docker to simplify setup, dependencies, and environment management.

---

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Setup and Installation](#setup-and-installation)
* [Running the Project](#running-the-project)
* [Using pgAdmin](#using-pgadmin)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* Python 3.13 based data ingestion script (`ingest_data.py`)
* Fully containerized for portability
* Uses `uv` for dependency management and execution
* Compatible with PostgreSQL database backend

---

## Prerequisites

Make sure you have the following installed:

* [Docker](https://www.docker.com/) (Engine + CLI)
* [Docker Compose](https://docs.docker.com/compose/) (if using `docker-compose`)
* Internet connection for pulling Docker images

---

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Build the Docker image

```bash
docker build -t my-ingestion-image .
```

This will:

* Pull the base Python 3.13 image
* Copy your project files into the container
* Install dependencies via `uv sync --locked`

### 3. Run the container

**Run interactively (for debugging or checking pip versions, etc.):**

```bash
docker run -it --entrypoint bash my-ingestion-image
```

## Using Docker Compose

If your project uses `docker-compose.yaml` with PostgreSQL / pgAdmin:

```bash
docker compose up -d
```

This will:

* Start PostgreSQL on port `5432`
* Start pgAdmin on port `5050` (or whichever is configured)
* Allow you to connect pgAdmin to Postgres using:

  * **Hostname:** `pgdatabase` (if using Compose network)
  * **Port:** `5432`
  * **Username/Password:** as defined in `docker-compose.yaml`

Stop all containers:

```bash
docker compose down
```

---

## Running the Project

Once the Docker container is running:

```bash
docker run -it --rm\
          --network=pg-network \
              my-ingestion-image:latest \
                --pg-user={username} \
                --pg-pass={password} \
                --pg-host=pgdatabase \
                --pg-port=5432 \
                --pg-db=ny_taxi \
                --target-table=green_taxi_trips
```

* This executes `ingest_data.py` automatically.
* Any logs or outputs are printed to your terminal.

---

## Using pgAdmin to Inspect Database

1. Open pgAdmin in your browser: `http://localhost:5050`
2. Register a new server with:

   * **Hostname:** `localhost` (or `pgdatabase` if in Docker Compose network)
   * **Port:** `5432`
   * **Username / Password:** as defined in Postgres environment variables
3. Expand the database → Schemas → Tables → use the Query Tool or View/Edit Data to inspect tables.

---

## Project Structure

```
project-directory/
│
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── ingest_data.py
├── docker-compose.yaml (optional)
└── README.md
```

* `Dockerfile` – builds the ingestion container
* `ingest_data.py` – main ingestion script
* `pyproject.toml` / `uv.lock` – project dependencies
* `docker-compose.yaml` – optional, starts Postgres + pgAdmin

---

## Contributing

* Fork the repository
* Create a branch for your feature
* Submit a pull request

---

## License

MIT License.

