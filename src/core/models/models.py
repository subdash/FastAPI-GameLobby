from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import relationship

from src.core.models.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=128), unique=True, index=True)
    email = Column(String(length=128), unique=True, index=True)
    hashed_password = Column(String(length=128))

    availability = relationship("Availability", back_populates="user")
    interest = relationship("Interest", back_populates="user")


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    time_avail = Column(DATETIME)

    user = relationship("User", back_populates="availability")


class Interest(Base):
    __tablename__ = "interest"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    game_id = Column(Integer, ForeignKey("game.id"))

    user = relationship("User", back_populates="interest")
    game = relationship("Game", back_populates="interest")


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=128), unique=True, index=True)
    min_players = Column(Integer)
    max_players = Column(Integer)

    interest = relationship("Interest", back_populates="game")

