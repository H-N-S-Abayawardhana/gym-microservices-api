from fastapi import APIRouter, HTTPException, status

from models import AttendanceCreate, AttendanceResponse, AttendanceUpdate


router = APIRouter()

# In-memory storage
attendance_db: list[AttendanceResponse] = []
attendance_counter: int = 1


@router.get("/", response_model=list[AttendanceResponse])
def list_attendance():
    return attendance_db


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: int):
    for record in attendance_db:
        if record.attendance_id == attendance_id:
            return record
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(payload: AttendanceCreate):
    global attendance_counter

    new_record = AttendanceResponse(attendance_id=attendance_counter, **payload.model_dump())
    attendance_db.append(new_record)
    attendance_counter += 1
    return new_record


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, payload: AttendanceUpdate):
    for idx, record in enumerate(attendance_db):
        if record.attendance_id == attendance_id:
            updated = AttendanceResponse(attendance_id=attendance_id, **payload.model_dump())
            attendance_db[idx] = updated
            return updated
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: int):
    for idx, record in enumerate(attendance_db):
        if record.attendance_id == attendance_id:
            attendance_db.pop(idx)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found")
