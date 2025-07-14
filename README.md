# ⚡ n8n + PostgreSQL Integration

This project integrates [n8n](https://n8n.io/) with a PostgreSQL database using Docker Compose, and includes:

- A Python backend for managing database models and migrations (via Alembic)
- Dockerized orchestration with PostgreSQL
- Automated seeding of test data
- An n8n workflow for importing `.zip` files with CSVs (clients, contracts, readings)
- Anomaly detection using Z-score

---

## 📦 Project Structure

```
n8n_postgres_integration/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml (Poetry)
├── src/
│   ├── config.py
│   ├── models/
│   ├── seed/
│   └── ...
├── migrations/
├── data/
│   ├── clientes.csv
│   ├── contratos.csv
│   ├── leituras.csv
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-user/n8n-postgres-integration.git
cd n8n-postgres-integration
```

### 2. Start the stack

```bash
docker compose up --build
```

This will:

- Start Postgres
- Run Alembic migrations
- Seed the database with initial data (if prompted)
- Launch n8n on [http://localhost:5678](http://localhost:5678)

---

## ⚙️ Services

| Service   | Port | Description                          |
|-----------|------|--------------------------------------|
| n8n       | 5678 | Workflow automation UI               |
| postgres  | 5432 | Main database                        |
| migrate   | —    | Runs Alembic migrations on startup   |
| seed      | —    | Populates database using ORM models  |

---

## 🧬 Python Tooling

### Dependency management via Poetry

```bash
poetry install
```

Make sure to install with:

```bash
poetry config virtualenvs.create false
```

---

## 📋 CSV Structure

The `data/` folder contains:

- `clientes.csv`: 10 clients (7 active)
- `contratos.csv`: client–contract mapping
- `leituras.csv`: energy readings, with 1 outliers

Use these files in the n8n `.zip` workflow to populate the database.

---

## 🔁 Workflow: Upload `.zip` and Populate DB

An n8n workflow is included that:

1. Accepts a `.zip` file via HTTP: POST http://localhost:5678/webhook-test/upload-seed
2. Unzips `clientes.csv`, `contratos.csv`, and `leituras.csv`
3. Parses and inserts the rows into Postgres

Use [Move Binary Data], [Split In Batches], and [Postgres Insert] nodes inside the workflow.

---

## 📊 Workflow: Detect Outliers in Readings

Another workflow:

- Fetches mean readings per active client (last 3 months)
- Calculates Z-score
- Detects outliers and returns JSON
- Feeds data to an AI agent for insight generation
- Triggered by: GET http://localhost:5678/webhook-test/get-results

---

## 🧪 Alembic Migrations

To create migrations:

```bash
alembic revision --autogenerate -m "create clients table"
```

To apply migrations:

```bash
alembic upgrade head
```

To downgrade:

```bash
alembic downgrade -1
```

These are not necessary to be executed, if the project is run by docker compose

---

## 🧑‍💻 Authors

- Rodrigo Rangel 🧙‍♂️
- With assistance from ChatGPT 😄

---

## 📄 License

MIT License
