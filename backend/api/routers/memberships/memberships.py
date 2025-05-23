from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import Membership, MembershipType

router = APIRouter(
    prefix="/memberships",
    tags=["Memberships"],
    responses={404: {"description": "Not found"}},
)

# Mock data
memberships = [
    Membership(
        id=1,
        type=MembershipType.BASIC,
        name="Basic Plan",
        description="Access to gym facilities during standard hours",
        price=29.99,
        duration_days=30,
        benefits=["Gym access", "Locker usage"]
    ),
    Membership(
        id=2,
        type=MembershipType.STANDARD,
        name="Standard Plan",
        description="Full access to gym and basic classes",
        price=49.99,
        duration_days=30,
        benefits=["Gym access", "Locker usage", "Basic classes", "Fitness assessment"]
    ),
    Membership(
        id=3,
        type=MembershipType.PREMIUM,
        name="Premium Plan",
        description="Complete access to all gym facilities and classes with personal training sessions",
        price=99.99,
        duration_days=30,
        benefits=["24/7 Gym access", "Locker usage", "All classes", "Personal training (2x/month)", "Nutrition consultation"]
    ),
]

@router.get("/", response_model=List[Membership])
async def get_memberships(
    skip: int = 0, 
    limit: int = 10,
    type: Optional[MembershipType] = None
):
    """
    Retrieve all membership plans with optional filtering by type.
    """
    if type:
        filtered_memberships = [m for m in memberships if m.type == type]
    else:
        filtered_memberships = memberships
    
    return filtered_memberships[skip : skip + limit]

@router.get("/{membership_id}", response_model=Membership)
async def get_membership(membership_id: int):
    """
    Retrieve a specific membership plan by ID.
    """
    for membership in memberships:
        if membership.id == membership_id:
            return membership
    raise HTTPException(status_code=404, detail="Membership not found")

@router.post("/", response_model=Membership)
async def create_membership(membership: Membership):
    """
    Create a new membership plan.
    """
    memberships.append(membership)
    return membership

@router.put("/{membership_id}", response_model=Membership)
async def update_membership(membership_id: int, membership: Membership):
    """
    Update an existing membership plan.
    """
    for i, m in enumerate(memberships):
        if m.id == membership_id:
            memberships[i] = membership
            return membership
    raise HTTPException(status_code=404, detail="Membership not found")

@router.delete("/{membership_id}")
async def delete_membership(membership_id: int):
    """
    Delete a membership plan.
    """
    for i, m in enumerate(memberships):
        if m.id == membership_id:
            memberships.pop(i)
            return {"message": "Membership deleted successfully"}
    raise HTTPException(status_code=404, detail="Membership not found")