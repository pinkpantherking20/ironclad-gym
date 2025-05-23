from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, date

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import Member, Gender

router = APIRouter(
    prefix="/members",
    tags=["Members"],
    responses={404: {"description": "Not found"}},
)

# Mock data
members = [
    Member(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="555-1234",
        gender=Gender.MALE,
        date_of_birth=date(1985, 5, 15),
        membership_id=1,
        join_date=datetime(2022, 1, 10),
        active=True
    ),
    Member(
        id=2,
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        phone="555-5678",
        gender=Gender.FEMALE,
        date_of_birth=date(1990, 8, 22),
        membership_id=2,
        join_date=datetime(2022, 3, 15),
        active=True
    ),
    Member(
        id=3,
        first_name="Michael",
        last_name="Johnson",
        email="michael.j@example.com",
        phone="555-9012",
        gender=Gender.MALE,
        date_of_birth=date(1978, 11, 30),
        membership_id=3,
        join_date=datetime(2021, 12, 5),
        active=False
    ),
]

@router.get("/", response_model=List[Member])
async def get_members(
    skip: int = 0, 
    limit: int = 10,
    active: Optional[bool] = None
):
    """
    Retrieve all gym members with optional filtering by active status.
    """
    if active is not None:
        filtered_members = [m for m in members if m.active == active]
    else:
        filtered_members = members
    
    return filtered_members[skip : skip + limit]

@router.get("/{member_id}", response_model=Member)
async def get_member(member_id: int):
    """
    Retrieve a specific member by ID.
    """
    for member in members:
        if member.id == member_id:
            return member
    raise HTTPException(status_code=404, detail="Member not found")

@router.post("/", response_model=Member)
async def create_member(member: Member):
    """
    Create a new member.
    """
    # In a real application, we would save to a database
    # For now, we'll just return the member with an ID
    members.append(member)
    return member

@router.put("/{member_id}", response_model=Member)
async def update_member(member_id: int, member: Member):
    """
    Update an existing member.
    """
    for i, m in enumerate(members):
        if m.id == member_id:
            members[i] = member
            return member
    raise HTTPException(status_code=404, detail="Member not found")

@router.delete("/{member_id}")
async def delete_member(member_id: int):
    """
    Delete a member.
    """
    for i, m in enumerate(members):
        if m.id == member_id:
            members.pop(i)
            return {"message": "Member deleted successfully"}
    raise HTTPException(status_code=404, detail="Member not found")