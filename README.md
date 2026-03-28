# Gym microservices

Monorepo layout for gym domain services and an API gateway.

## Layout

- **api-gateway** — entry HTTP API; compose calls to downstream services.
- **member-service**, **trainer-service**, **workout-plan-service**, **booking-service**, **diet-plan-service**, **attendance-service** — domain microservices.

Each service has its own `requirements.txt`. **Always run Uvicorn from that service’s folder** so `main.py` is found.

### Booking service (port 8010)

```bash
cd booking-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8010
```

Swagger: http://127.0.0.1:8010/docs

### API gateway

Point the gateway at the booking service (default matches port **8010**):

```bash
cd api-gateway
pip install -r requirements.txt
# Optional if booking runs elsewhere:
# set BOOKING_SERVICE_URL=http://127.0.0.1:8010
uvicorn main:app --reload --port 8000
```

Swagger: http://127.0.0.1:8000/docs — `/bookings` proxies to the booking microservice.

### Other services

```bash
cd member-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```
