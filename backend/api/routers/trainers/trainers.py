from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from models import Trainer

router = APIRouter(
    prefix="/trainers",
    tags=["Trainers"],
    responses={404: {"description": "Not found"}},
)

# Mock data
trainers = [
    Trainer(
        id=1,
        first_name="Alex",
        last_name="Johnson",
        email="alex.j@ironclad.com",
        phone="555-1111",
        specialization=["Yoga", "Pilates"],
        experience_years=5,
        bio="Certified yoga instructor with focus on mindfulness and flexibility.",
        available=True
    ),
    Trainer(
        id=2,
        first_name="Sarah",
        last_name="Williams",
        email="sarah.w@ironclad.com",
        phone="555-2222",
        specialization=["HIIT", "Strength Training"],
        experience_years=8,
        bio="Former competitive athlete specializing in high-intensity workouts.",
        available=True
    ),
    Trainer(
        id=3,
        first_name="Marcus",
        last_name="Chen",
        email="marcus.c@ironclad.com",
        phone="555-3333",
        specialization=["Spinning", "Cardio"],
        experience_years=6,
        bio="Passionate about helping clients achieve their cardio fitness goals.",
        available=False
    ),
]

@router.get("/", response_model=List[Trainer])
async def get_trainers(
    skip: int = 0, 
    limit: int = 10,
    available: Optional[bool] = None,
    specialization: Optional[str] = None
):
    """
    Retrieve all trainers with optional filtering by availability and specialization.
    """
    filtered_trainers = trainers
    
    if available is not None:
        filtered_trainers = [t for t in filtered_trainers if t.available == available]
    
    if specialization:
        filtered_trainers = [t for t in filtered_trainers if specialization in t.specialization]
    
    return filtered_trainers[skip : skip + limit]

@router.get("/{trainer_id}", response_model=Trainer)
async def get_trainer(trainer_id: int):
    """
    Retrieve a specific trainer by ID.
    """
    for trainer in trainers:
        if trainer.id == trainer_id:
            return trainer
    raise HTTPException(status_code=404, detail="Trainer not found")

@router.post("/", response_model=Trainer)
async def create_trainer(trainer: Trainer):
    """
    Add a new trainer to the gym.
    """
    trainers.append(trainer)
    return trainer

@router.put("/{trainer_id}", response_model=Trainer)
async def update_trainer(trainer_id: int, trainer: Trainer):
    """
    Update an existing trainer's information.
    """
    for i, t in enumerate(trainers):
        if t.id == trainer_id:
            trainers[i] = trainer
            return trainer
    raise HTTPException(status_code=404, detail="Trainer not found")

@router.delete("/{trainer_id}")
async def delete_trainer(trainer_id: int):
    """
    Remove a trainer from the system.
    """
    for i, t in enumerate(trainers):
        if t.id == trainer_id:
            trainers.pop(i)
            return {"message": "Trainer deleted successfully"}
    raise HTTPException(status_code=404, detail="Trainer not found")