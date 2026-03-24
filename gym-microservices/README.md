# Gym microservices

Monorepo layout for gym domain services and an API gateway.

## Layout

- **api-gateway** — entry HTTP API; compose calls to downstream services.
- **member-service**, **trainer-service**, **workout-plan-service**, **booking-service**, **diet-plan-service**, **attendance-service** — domain microservices.

Each service has its own `requirements.txt`. Run locally with Uvicorn from the service directory, for example:

```bash
cd member-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```
