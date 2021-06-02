from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.models import crud
from src.core.schemas import schema
from src.v1.dependencies import get_db

router = APIRouter(prefix="/interest", tags=['interest'])


@router.post("/", response_model=schema.Interest)
async def create_interest(interest: schema.InterestCreate, db: Session = Depends(get_db)):
    """
    Endpoint for posting a game that a user is interested in playing.

    :param interest: user-id and game-id
    :param db: database dependency
    :return: JSON response of created interest
    """
    created_interest = crud.create_interest(db, interest.user_id, interest.game_id)

    return created_interest
