# Gym microservices

Monorepo of FastAPI microservices for a gym domain, plus an **API gateway** as the main HTTP entry point.

## Prerequisites

- **Python 3.10+** (3.12 is fine)
- **pip**

Optional: create a virtual environment per service or one at the repo root so dependencies stay isolated.

**Important:** Always `cd` into a service folder before installing or running Uvicorn so `main.py` resolves correctly.

---

## Services overview

| Service | Port | Responsibility | Main API prefix (direct service) |
|--------|------|----------------|----------------------------------|
| **api-gateway** | `8010` | Single entry URL; proxies requests to all domain microservices | `/members`, `/trainers`, `/workout-plans`, `/bookings`, `/diet-plans`, `/attendance` |
| **booking-service** | `8011` | Session bookings (in-memory MVP) | `/bookings` |
| **trainer-service** | `8012` | Trainers CRUD (in-memory) | `/trainers` |
| **workout-plan-service** | `8013` | Workout plans CRUD (in-memory) | `/workout-plans` |
| **attendance-service** | `8014` | Attendance (stub list) | `/attendance` |
| **diet-plan-service** | `8015` | Diet plans (stub list) | `/diet-plans` |
| **member-service** | `8016` | Members (stub list) | `/members` |

**Swagger UI** for any service: open `http://127.0.0.1:<port>/docs` after it is running.

**Gateway and booking:** The gateway reads `BOOKING_SERVICE_URL` (default `http://127.0.0.1:8011`, matching this repo’s booking service port). Override it if you run booking on another host or port.

---

## How to run each service

Use a **separate terminal** per process. From the repository root:

### api-gateway

```bash
cd api-gateway
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8010
```

- Docs: http://127.0.0.1:8010/docs  
- Health: http://127.0.0.1:8010/health  
- You can also run: `python main.py` (starts on port 8010).

If the booking service runs on another host or port, set `BOOKING_SERVICE_URL` before starting (see below).

### booking-service

```bash
cd booking-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8011
```

- Docs: http://127.0.0.1:8011/docs  
- You can also run: `python main.py` (starts on port 8011).

### trainer-service

```bash
cd trainer-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8012
```

- Docs: http://127.0.0.1:8012/docs  

### workout-plan-service

```bash
cd workout-plan-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8013
```

- Docs: http://127.0.0.1:8013/docs  

### attendance-service

```bash
cd attendance-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8014
```

- Docs: http://127.0.0.1:8014/docs  

### diet-plan-service

```bash
cd diet-plan-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8015
```

- Docs: http://127.0.0.1:8015/docs  

### member-service

```bash
cd member-service
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8016
```

- Docs: http://127.0.0.1:8016/docs  

---

## Environment variables (API gateway)

**`BOOKING_SERVICE_URL`** — Base URL of the booking microservice (no trailing slash). Default is `http://127.0.0.1:8011`. Set this only if booking runs elsewhere.

**Bash / macOS / Linux:**

```bash
export BOOKING_SERVICE_URL=http://127.0.0.1:8011
cd api-gateway
uvicorn main:app --reload --host 0.0.0.0 --port 8010
```

**PowerShell (Windows):**

```powershell
$env:BOOKING_SERVICE_URL = "http://127.0.0.1:8011"
cd api-gateway
uvicorn main:app --reload --host 0.0.0.0 --port 8010
```

**cmd.exe (Windows):**

```cmd
set BOOKING_SERVICE_URL=http://127.0.0.1:8011
cd api-gateway
uvicorn main:app --reload --host 0.0.0.0 --port 8010
```

---

## PostgreSQL setup (all microservices)

All six domain services now use PostgreSQL via `DATABASE_URL`.

**Fallback:** Each service’s `db.py` loads `DATABASE_URL` from a **`.env`** file in that service folder (e.g. `booking-service/.env`) if the shell variable is not set. Priority: shell env first, then `.env`.

You can set the URL in each terminal **before** starting a domain service:

```powershell
$env:DATABASE_URL = "postgresql://neondb_owner:...@ep-dark-poetry-amhgpm3s-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
```

Create tables once using:

```powershell
psql "postgresql://neondb_owner:...@ep-dark-poetry-amhgpm3s-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" -f database/schema.sql
```

`database/schema.sql` contains all service-owned tables.

---

## Typical local setup

1. Start all six microservices (`8011` to `8016`).  
2. Start **api-gateway** on `8010`.  
3. Call endpoints through the gateway, e.g. `GET http://127.0.0.1:8010/bookings`, `GET http://127.0.0.1:8010/members`, `GET http://127.0.0.1:8010/workout-plans`.

The gateway routes now forward to downstream services:
- `/bookings` -> booking-service (`8011`)
- `/trainers` -> trainer-service (`8012`)
- `/workout-plans` -> workout-plan-service (`8013`)
- `/attendance` -> attendance-service (`8014`)
- `/diet-plans` -> diet-plan-service (`8015`)
- `/members` -> member-service (`8016`)

---

## Layout

- `api-gateway/` — Gateway app and route modules.  
- `booking-service/`, `member-service/`, `trainer-service/`, `workout-plan-service/`, `diet-plan-service/`, `attendance-service/` — Each has its own `requirements.txt`, `main.py`, and routes/models as applicable.
