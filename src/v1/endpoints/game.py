from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.core.models import crud
from src.core.schemas import schema
from src.v1.dependencies import get_db

router = APIRouter(
    prefix="/games",
    tags=['game']
)


@router.get("/", response_model=List[schema.Game])
async def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint for retrieving the available list of games to play.

    :param skip: how many games to skip
    :param limit: how many total games
    :param db: database dependency
    :return: JSON response of a set of Game db objects
    """
    games = crud.get_games(db, skip=skip, limit=limit)

    return games
