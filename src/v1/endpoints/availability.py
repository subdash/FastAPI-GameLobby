from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.core.models import crud
from src.core.schemas import schema
from src.v1.dependencies import get_db

router = APIRouter(prefix="/availability", tags=['availability'])


@router.post("/", response_model=schema.Availability)
async def create_availability(availability: schema.AvailabilityCreate, db: Session = Depends(get_db)):
    """
    Endpoint for creating a time-slot representing an available time to play a
    game.

    :param availability: user-id and datetime
    :param db: database dependency
    :return: JSON response of created availability
    """
    created_availability = crud.create_availability(db, availability)

    return created_availability
