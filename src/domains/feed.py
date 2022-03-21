"""Feature: feed."""
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FeedModel(Base):
    """Feed model."""

    __tablename__ = "feed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    origin = Column(String(25))
    event = Column(String(25))
    description = Column(String(255))
    # date_time: Column(DateTime(timezone=True))

    def __repr__(self):
        """Feed representation."""
        return f"{self.__class__.__name__}(id={self.id}, " \
               f"origin={self.origin}, event={self.event}, " \
               f"description={self.description})"


class Feed(BaseModel):
    """Base Feed DTO."""

    origin: str
    event: str
    description: str


class FeedDetail(Feed):
    """Feed detail."""

    id: Optional[int] = None
    # date_time: datetime.datetime


class FeedExceptions(Exception):
    """Base exceptions for Feed."""


class FeedCreateError(FeedExceptions):
    """Raise when trying to create a new feed."""
