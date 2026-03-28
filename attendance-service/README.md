# Attendance Service

FastAPI microservice for managing gym attendance records using in-memory storage. Includes CRUD APIs and a simple API Gateway for forwarding attendance traffic.

## Project Structure

```
attendance-service/
├─ main.py           # FastAPI app entrypoint (runs on port 8014)
├─ routes.py         # Attendance CRUD routes (in-memory store)
├─ models.py         # Pydantic models & validation
├─ gateway.py        # Simple API gateway (forwards /attendance to service, port 8010)
├─ requirements.txt  # Python dependencies
```

## Data Model

- `attendance_id` (int, auto-increment)
- `member_id` (int)
- `trainer_id` (int, optional)
- `session_type` (string enum: `gym`, `personal_training`, `class`)
- `date` (string, e.g., `2026-03-25`)
- `check_in_time` (string, e.g., `09:00`)
- `status` (string)

## API Endpoints (Attendance Service)

Base path: `http://localhost:8014`

- `GET /attendance` — list all records
- `GET /attendance/{attendance_id}` — fetch one
- `POST /attendance` — create
- `PUT /attendance/{attendance_id}` — update
- `DELETE /attendance/{attendance_id}` — delete
- `GET /health` — health check

### Sample Payload

```json
{
  "member_id": 1,
  "trainer_id": 10,
  "session_type": "personal_training",
  "date": "2026-03-25",
  "check_in_time": "09:00",
  "status": "checked_in"
}
```

## API Gateway

- Runs on `http://localhost:8010`
- Forwards `/attendance` routes to `http://localhost:8014/attendance`
- Endpoints mirror the attendance service (GET/POST/PUT/DELETE, plus `GET /health`).
- Uses a Pydantic `Attendance` model on POST/PUT so Swagger shows the JSON request body schema.

## Running Locally

1. Install deps

```bash
pip install -r requirements.txt
```

2. Start Attendance Service (port 8014)

```bash
uvicorn main:app --host 0.0.0.0 --port 8014 --reload
```

3. Start API Gateway (port 8010)

```bash
uvicorn gateway:app --host 0.0.0.0 --port 8010 --reload
```

## Swagger / Docs

- Attendance Service docs: `http://localhost:8014/docs`
- Gateway docs: `http://localhost:8010/docs`

## Notes on Integration with Other Services

- `member_id` references the Member Service; `trainer_id` references the Trainer Service.
- In a fuller implementation, the Attendance Service could call those services (e.g., REST) to validate IDs or enrich responses before persisting. Here, storage is in-memory for simplicity.

## Health Checks

- Service: `GET /health` (port 8014)
- Gateway: `GET /health` (port 8010)
