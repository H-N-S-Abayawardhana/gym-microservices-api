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
| **api-gateway** | `8010` | Single entry URL; proxies **bookings** to the booking service; other paths are in-process stubs for now | `/members`, `/trainers`, `/workouts`, `/bookings`, `/diet`, `/attendance` |
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

## Typical local setup

1. Start **booking-service** on `8011`.  
2. Start **api-gateway** on `8010` (defaults already point at `http://127.0.0.1:8011`).  
3. Call bookings through the gateway, e.g. `GET http://127.0.0.1:8010/bookings`, which forwards to the booking service.

Other microservices can be run on their ports when you call them **directly**; the gateway’s `/members`, `/trainers`, `/workouts`, `/diet`, and `/attendance` routes are placeholders until wired to those services.

---

## Layout

- `api-gateway/` — Gateway app and route modules.  
- `booking-service/`, `member-service/`, `trainer-service/`, `workout-plan-service/`, `diet-plan-service/`, `attendance-service/` — Each has its own `requirements.txt`, `main.py`, and routes/models as applicable.
