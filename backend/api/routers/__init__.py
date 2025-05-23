# This file makes the directory a Python package
from .members.members import router as members_router
from .classes.classes import router as classes_router
from .equipment.equipment import router as equipment_router
from .trainers.trainers import router as trainers_router
from .memberships.memberships import router as memberships_router