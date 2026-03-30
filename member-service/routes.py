from fastapi import APIRouter, HTTPException
from db import get_conn
from models import Member, MemberCreate, MemberUpdate

router = APIRouter()


@router.get("/", response_model=list[Member])
def get_all_members():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, email, phone, membership_type, age
                FROM members
                ORDER BY id;
                """
            )
            rows = cur.fetchall()
    return [Member(**row) for row in rows]


@router.get("/{member_id}", response_model=Member)
def get_member(member_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, email, phone, membership_type, age
                FROM members
                WHERE id = %s;
                """,
                (member_id,),
            )
            row = cur.fetchone()
    if row:
        return Member(**row)
    raise HTTPException(status_code=404, detail="Member not found")


@router.post("/", response_model=Member, status_code=201)
def create_member(member: MemberCreate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO members (name, email, phone, membership_type, age)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, name, email, phone, membership_type, age;
                """,
                (
                    member.name,
                    member.email,
                    member.phone,
                    member.membership_type,
                    member.age,
                ),
            )
            row = cur.fetchone()
        conn.commit()
    return Member(**row)


@router.put("/{member_id}", response_model=Member)
def update_member(member_id: int, updated_data: MemberUpdate):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, email, phone, membership_type, age
                FROM members
                WHERE id = %s;
                """,
                (member_id,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Member not found")
            current = Member(**row)
            cur.execute(
                """
                UPDATE members
                SET name = %s,
                    email = %s,
                    phone = %s,
                    membership_type = %s,
                    age = %s
                WHERE id = %s
                RETURNING id, name, email, phone, membership_type, age;
                """,
                (
                    updated_data.name if updated_data.name is not None else current.name,
                    str(updated_data.email) if updated_data.email is not None else str(current.email),
                    updated_data.phone if updated_data.phone is not None else current.phone,
                    updated_data.membership_type
                    if updated_data.membership_type is not None
                    else current.membership_type,
                    updated_data.age if updated_data.age is not None else current.age,
                    member_id,
                ),
            )
            updated = cur.fetchone()
        conn.commit()
    return Member(**updated)


@router.delete("/{member_id}")
def delete_member(member_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM members
                WHERE id = %s
                RETURNING id, name, email, phone, membership_type, age;
                """,
                (member_id,),
            )
            row = cur.fetchone()
        conn.commit()
    if row:
        return {"message": "Member deleted successfully", "member": row}
    raise HTTPException(status_code=404, detail="Member not found")