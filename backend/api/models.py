from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class MembershipType(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"

class Member(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    gender: Gender
    date_of_birth: date
    membership_id: int
    join_date: datetime
    active: bool = True

class Trainer(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    specialization: List[str]
    experience_years: int
    bio: str
    available: bool = True

class ClassType(str, Enum):
    YOGA = "yoga"
    PILATES = "pilates"
    ZUMBA = "zumba"
    HIIT = "hiit"
    SPINNING = "spinning"
    BOXING = "boxing"
    STRENGTH = "strength"

class GymClass(BaseModel):
    id: int
    name: str
    description: str
    class_type: ClassType
    trainer_id: int
    capacity: int
    duration_minutes: int
    schedule_time: datetime
    current_bookings: int = 0

class Equipment(BaseModel):
    id: int
    name: str
    description: str
    category: str
    purchase_date: date
    last_maintenance: date
    status: str
    quantity: int

class Membership(BaseModel):
    id: int
    type: MembershipType
    name: str
    description: str
    price: float
    duration_days: int
    benefits: List[str]