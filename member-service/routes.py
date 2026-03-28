from fastapi import APIRouter, HTTPException
from models import Member, MemberCreate, MemberUpdate

router = APIRouter()

members = [
    {
        "id": 1,
        "name": "John Silva",
        "email": "john@example.com",
        "phone": "0771234567",
        "membership_type": "Monthly",
        "age": 25
    },
    {
        "id": 2,
        "name": "Nethu Perera",
        "email": "nethu@example.com",
        "phone": "0719876543",
        "membership_type": "Annual",
        "age": 30
    }
]


@router.get("/", response_model=list[Member])
def get_all_members():
    return members


@router.get("/{member_id}", response_model=Member)
def get_member(member_id: int):
    for member in members:
        if member["id"] == member_id:
            return member
    raise HTTPException(status_code=404, detail="Member not found")


@router.post("/", response_model=Member, status_code=201)
def create_member(member: MemberCreate):
    new_id = max([m["id"] for m in members], default=0) + 1
    new_member = {
        "id": new_id,
        "name": member.name,
        "email": member.email,
        "phone": member.phone,
        "membership_type": member.membership_type,
        "age": member.age
    }
    members.append(new_member)
    return new_member


@router.put("/{member_id}", response_model=Member)
def update_member(member_id: int, updated_data: MemberUpdate):
    for member in members:
        if member["id"] == member_id:
            if updated_data.name is not None:
                member["name"] = updated_data.name
            if updated_data.email is not None:
                member["email"] = updated_data.email
            if updated_data.phone is not None:
                member["phone"] = updated_data.phone
            if updated_data.membership_type is not None:
                member["membership_type"] = updated_data.membership_type
            if updated_data.age is not None:
                member["age"] = updated_data.age
            return member
    raise HTTPException(status_code=404, detail="Member not found")


@router.delete("/{member_id}")
def delete_member(member_id: int):
    for index, member in enumerate(members):
        if member["id"] == member_id:
            deleted_member = members.pop(index)
            return {"message": "Member deleted successfully", "member": deleted_member}
    raise HTTPException(status_code=404, detail="Member not found")