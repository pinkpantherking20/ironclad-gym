from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import Equipment

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"],
    responses={404: {"description": "Not found"}},
)

# Mock data
equipment = [
    Equipment(
        id=1,
        name="Treadmill",
        description="Commercial grade treadmill with incline function",
        category="Cardio",
        purchase_date=date(2021, 5, 15),
        last_maintenance=date(2023, 1, 10),
        status="Operational",
        quantity=8
    ),
    Equipment(
        id=2,
        name="Dumbbells Set",
        description="Set of dumbbells ranging from 5kg to 30kg",
        category="Strength",
        purchase_date=date(2020, 11, 8),
        last_maintenance=date(2022, 11, 8),
        status="Operational",
        quantity=10
    ),
    Equipment(
        id=3,
        name="Rowing Machine",
        description="Water resistance rowing machine",
        category="Cardio",
        purchase_date=date(2022, 2, 20),
        last_maintenance=date(2023, 2, 20),
        status="Under Maintenance",
        quantity=4
    ),
]

@router.get("/", response_model=List[Equipment])
async def get_equipment(
    skip: int = 0, 
    limit: int = 10,
    status: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Retrieve all gym equipment with optional filtering by status and category.
    """
    filtered_equipment = equipment
    
    if status:
        filtered_equipment = [e for e in filtered_equipment if e.status == status]
    
    if category:
        filtered_equipment = [e for e in filtered_equipment if e.category == category]
    
    return filtered_equipment[skip : skip + limit]

@router.get("/{equipment_id}", response_model=Equipment)
async def get_equipment_item(equipment_id: int):
    """
    Retrieve a specific equipment item by ID.
    """
    for item in equipment:
        if item.id == equipment_id:
            return item
    raise HTTPException(status_code=404, detail="Equipment not found")

@router.post("/", response_model=Equipment)
async def create_equipment(item: Equipment):
    """
    Add new equipment to the inventory.
    """
    equipment.append(item)
    return item

@router.put("/{equipment_id}", response_model=Equipment)
async def update_equipment(equipment_id: int, item: Equipment):
    """
    Update existing equipment details.
    """
    for i, e in enumerate(equipment):
        if e.id == equipment_id:
            equipment[i] = item
            return item
    raise HTTPException(status_code=404, detail="Equipment not found")

@router.delete("/{equipment_id}")
async def delete_equipment(equipment_id: int):
    """
    Remove equipment from inventory.
    """
    for i, e in enumerate(equipment):
        if e.id == equipment_id:
            equipment.pop(i)
            return {"message": "Equipment deleted successfully"}
    raise HTTPException(status_code=404, detail="Equipment not found")