from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import GymClass, ClassType

router = APIRouter(
    prefix="/classes",
    tags=["Classes"],
    responses={404: {"description": "Not found"}},
)

# Mock data - current date for scheduling
now = datetime.now()

classes = [
    GymClass(
        id=1,
        name="Morning Yoga",
        description="Start your day with energizing yoga poses and breathing exercises.",
        class_type=ClassType.YOGA,
        trainer_id=1,
        capacity=20,
        duration_minutes=60,
        schedule_time=now + timedelta(days=1, hours=8),
        current_bookings=12
    ),
    GymClass(
        id=2,
        name="HIIT Blast",
        description="High-intensity interval training to maximize calorie burn.",
        class_type=ClassType.HIIT,
        trainer_id=2,
        capacity=15,
        duration_minutes=45,
        schedule_time=now + timedelta(days=1, hours=17, minutes=30),
        current_bookings=8
    ),
    GymClass(
        id=3,
        name="Spin Class",
        description="Indoor cycling workout with energetic music and motivation.",
        class_type=ClassType.SPINNING,
        trainer_id=3,
        capacity=12,
        duration_minutes=50,
        schedule_time=now + timedelta(days=2, hours=18),
        current_bookings=10
    ),
]

@router.get("/", response_model=List[GymClass])
async def get_classes(
    skip: int = 0, 
    limit: int = 10,
    class_type: Optional[ClassType] = None
):
    """
    Retrieve all gym classes with optional filtering by class type.
    """
    if class_type:
        filtered_classes = [c for c in classes if c.class_type == class_type]
    else:
        filtered_classes = classes
    
    return filtered_classes[skip : skip + limit]

@router.get("/{class_id}", response_model=GymClass)
async def get_class(class_id: int):
    """
    Retrieve a specific class by ID.
    """
    for cls in classes:
        if cls.id == class_id:
            return cls
    raise HTTPException(status_code=404, detail="Class not found")

@router.post("/", response_model=GymClass)
async def create_class(gym_class: GymClass):
    """
    Create a new gym class.
    """
    classes.append(gym_class)
    return gym_class

@router.put("/{class_id}", response_model=GymClass)
async def update_class(class_id: int, gym_class: GymClass):
    """
    Update an existing gym class.
    """
    for i, c in enumerate(classes):
        if c.id == class_id:
            classes[i] = gym_class
            return gym_class
    raise HTTPException(status_code=404, detail="Class not found")

@router.delete("/{class_id}")
async def delete_class(class_id: int):
    """
    Delete a gym class.
    """
    for i, c in enumerate(classes):
        if c.id == class_id:
            classes.pop(i)
            return {"message": "Class deleted successfully"}
    raise HTTPException(status_code=404, detail="Class not found")