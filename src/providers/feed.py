"""Feature: feed."""
from typing import List, Optional

from databases import Database
from sqlalchemy import select, insert

from src.domains.feed import FeedDetail, FeedModel, FeedCreateError, Feed
from src.interfaces.feed import SimpleFeedInterface


class SimpleFeedProvider(SimpleFeedInterface):
    """Simple feed providers."""

    POSTGRES_HOST = "database"
    POSTGRES_PORT = 5432
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = "SuperSecret"
    POSTGRES_DB = "simple_feed_db"
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}" \
                   f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    database = Database(DATABASE_URL)

    async def read_feeds(self) -> List[FeedDetail]:
        """
        Read feeds.

        Returns:
            A list of FeedDetail DTO
        """
        query = select(FeedModel)
        async with self.database as db:
            result: List[FeedModel] = await db.fetch_all(query=query)  # Noqa
            return [FeedDetail(
                id=feed.id,
                origin=feed.origin,
                event=feed.event,
                description=feed.description,
            ) for feed in result]

    async def read_feed_by_id(self, feed_id: int) -> Optional[FeedDetail]:
        """
        Read feed by id.

        Args:
            feed_id: A feed id

        Returns:
            A FeedDetail DTO or None
        """
        query = select(FeedModel).where(FeedModel.id.__eq__(feed_id))

        async with self.database as db:
            result: List[FeedModel] = await db.fetch_all(query=query)  # Noqa

        feeds = [FeedDetail(
            id=feed.id,
            origin=feed.origin,
            event=feed.event,
            description=feed.description,
        ) for feed in result]

        if not feeds:
            return None

        return feeds[0]

    async def create_feed(self, feed: Feed) -> int:
        """
        Create a new feed.

        Args:
            feed: A Feed DTO.

        Returns:
            A key id
        """
        try:
            query = insert(FeedModel)
            values = feed.dict()
            async with self.database as db:
                result = await db.execute(query=query, values=values)
            return result

        except Exception as exc:
            raise FeedCreateError(f"Unable to create a new feed. {exc}")
