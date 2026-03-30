# Swagger Endpoint Test Guide (Clear Step-by-Step)

Use this file to test **every endpoint** in all services and in the API gateway.

---

## 1) Prerequisites

1. Start PostgreSQL (Neon) connection for each service (`DATABASE_URL` via terminal env or `.env`).
2. Create tables once:
   - Run `database/schema.sql` against your DB.
3. Start all services:
   - Booking `8011`, Trainer `8012`, Workout `8013`, Attendance `8014`, Diet `8015`, Member `8016`, Gateway `8010`.

---

## 2) Swagger URLs

| System | URL |
|---|---|
| API Gateway | `http://127.0.0.1:8010/docs` |
| Booking Service | `http://127.0.0.1:8011/docs` |
| Trainer Service | `http://127.0.0.1:8012/docs` |
| Workout Plan Service | `http://127.0.0.1:8013/docs` |
| Attendance Service | `http://127.0.0.1:8014/docs` |
| Diet Plan Service | `http://127.0.0.1:8015/docs` |
| Member Service | `http://127.0.0.1:8016/docs` |

---

## 3) How to execute any endpoint in Swagger

1. Open `/docs`.
2. Expand endpoint row.
3. Click **Try it out**.
4. Add path parameter or request JSON (if needed).
5. Click **Execute**.
6. Confirm response code (`200`, `201`, etc.) and response body.

---

## 4) Test Data You Can Reuse

### Member create
```json
{
  "name": "Test Member",
  "email": "test.member@example.com",
  "phone": "0770000000",
  "membership_type": "Monthly",
  "age": 28
}
```

### Member update
```json
{
  "name": "Test Member Updated",
  "email": "test.member@example.com",
  "phone": "0770000001",
  "membership_type": "Annual",
  "age": 29
}
```

### Trainer create / update
```json
{
  "name": "Coach Silva",
  "specialty": "Strength",
  "phone": "0771111111",
  "availability": "Mon-Fri 9-17"
}
```

### Workout create / update
```json
{
  "member_id": 1,
  "trainer_id": 1,
  "goal": "Build endurance",
  "duration_weeks": 8,
  "difficulty_level": "Intermediate",
  "notes": "3 sessions per week"
}
```

### Booking create
```json
{
  "member_id": 1,
  "trainer_id": 1,
  "session_date": "2026-04-15",
  "session_time": "10:00",
  "booking_status": "Confirmed"
}
```

### Booking update
```json
{
  "member_id": 1,
  "trainer_id": 1,
  "session_date": "2026-04-16",
  "session_time": "11:00",
  "booking_status": "Cancelled"
}
```

### Diet create / update
```json
{
  "member_id": "1",
  "trainer_id": "trainer-uuid-here",
  "goal": "Weight loss",
  "meal_plan": "High protein, 2000 kcal",
  "duration_weeks": 12
}
```

### Attendance create / update
```json
{
  "member_id": "1",
  "checked_in_at": "2026-03-30T09:15:00"
}
```

---

## 5) Direct Service Endpoint Checklist (test every endpoint)

Use this exact order for each service: **GET list -> POST -> GET by id -> PUT -> DELETE**.

### 5.1 Member Service (`8016`)
- `GET /members/`
- `POST /members/` (save returned `id` as `member_id`)
- `GET /members/{member_id}`
- `PUT /members/{member_id}`
- `DELETE /members/{member_id}`

### 5.2 Trainer Service (`8012`)
- `GET /trainers/`
- `POST /trainers/` (save returned `trainer_id`)
- `GET /trainers/{trainer_id}`
- `PUT /trainers/{trainer_id}`
- `DELETE /trainers/{trainer_id}`

### 5.3 Workout Plan Service (`8013`)
- `GET /workout-plans/`
- `POST /workout-plans/` (save returned `plan_id`)
- `GET /workout-plans/{plan_id}`
- `PUT /workout-plans/{plan_id}`
- `DELETE /workout-plans/{plan_id}`

### 5.4 Booking Service (`8011`)
- `GET /bookings`
- `POST /bookings` (save returned `booking_id`)
- `GET /bookings/{booking_id}`
- `PUT /bookings/{booking_id}`
- `DELETE /bookings/{booking_id}`

### 5.5 Diet Plan Service (`8015`)
- `GET /diet-plans/`
- `POST /diet-plans/` (save `item.diet_plan_id`)
- `GET /diet-plans/{diet_plan_id}`
- `PUT /diet-plans/{diet_plan_id}`
- `DELETE /diet-plans/{diet_plan_id}`

### 5.6 Attendance Service (`8014`)
- `GET /attendance/`
- `POST /attendance/` (save `item.id` as `attendance_id`)
- `GET /attendance/{attendance_id}`
- `PUT /attendance/{attendance_id}`
- `DELETE /attendance/{attendance_id}`

---

## 6) Gateway Endpoint Checklist (`8010/docs`)

Repeat the same endpoint checks in gateway Swagger:

### Members (via gateway)
- `GET /members`
- `POST /members`
- `GET /members/{member_id}`
- `PUT /members/{member_id}`
- `DELETE /members/{member_id}`

### Trainers (via gateway)
- `GET /trainers`
- `POST /trainers`
- `GET /trainers/{trainer_id}`
- `PUT /trainers/{trainer_id}`
- `DELETE /trainers/{trainer_id}`

### Workout Plans (via gateway)
- `GET /workout-plans`
- `POST /workout-plans`
- `GET /workout-plans/{plan_id}`
- `PUT /workout-plans/{plan_id}`
- `DELETE /workout-plans/{plan_id}`

### Bookings (via gateway)
- `GET /bookings`
- `POST /bookings`
- `GET /bookings/{booking_id}`
- `PUT /bookings/{booking_id}`
- `DELETE /bookings/{booking_id}`

### Diet Plans (via gateway)
- `GET /diet-plans`
- `POST /diet-plans`
- `GET /diet-plans/{diet_plan_id}`
- `PUT /diet-plans/{diet_plan_id}`
- `DELETE /diet-plans/{diet_plan_id}`

### Attendance (via gateway)
- `GET /attendance`
- `POST /attendance`
- `GET /attendance/{attendance_id}`
- `PUT /attendance/{attendance_id}`
- `DELETE /attendance/{attendance_id}`

---

## 7) Screenshot Plan for Assignment (easy)

For each domain (member, trainer, workout, booking, diet, attendance):
1. Take 1 screenshot from direct service Swagger (`8011`-`8016`) after successful execute.
2. Take 1 screenshot from gateway Swagger (`8010`) for the same operation.
3. Keep response code and JSON visible in screenshot.

Minimum recommended shots:
- `GET list` direct + gateway for all 6 domains.
- `POST create` direct + gateway for at least 2-3 domains.

---

## 8) Common Errors

| Error | Meaning | Fix |
|---|---|---|
| `500` from service startup | `DATABASE_URL` missing | Set env or `.env` in that service folder |
| `500` from gateway endpoint | downstream service not running | start the target service |
| `404` by id | wrong/old id | use latest id returned by POST |
| `422` | invalid body format/type | copy sample JSON exactly |

