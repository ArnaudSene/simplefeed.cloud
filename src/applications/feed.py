"""Feature: feed."""

from typing import List, Optional

from src.domains.feed import FeedDetail, Feed
from src.interfaces.feed import SimpleFeedInterface


class ReadFeeds:
    """Read feeds."""

    def __init__(
            self,
            feed_provider: SimpleFeedInterface
    ):
        """Init."""
        self.feed_provider = feed_provider

    async def __call__(self) -> List[FeedDetail]:
        """
        Read feeds.

        Returns:
            A list of FeedDetail DTO.
        """
        return await self.feed_provider.read_feeds()


class ReadFeedById:
    """Read feed by id."""

    def __init__(
            self,
            feed_provider: SimpleFeedInterface
    ):
        """Init."""
        self.feed_provider = feed_provider

    async def __call__(self, feed_id: int) -> Optional[FeedDetail]:
        """
        Read feed by id.

        Returns:
            A FeedDetail DTO or None
        """
        return await self.feed_provider.read_feed_by_id(feed_id=feed_id)


class CreateNewFeed:
    """Create a new feed."""

    def __init__(
            self,
            feed_provider: SimpleFeedInterface
    ):
        """Init."""
        self.feed_provider = feed_provider

    async def __call__(self, feed: Feed) -> int:
        """
        Create a new feed.

        Args:
            feed: A Feed DTO.

        Returns:
            A feed id
        """
        return await self.feed_provider.create_feed(feed=feed)


class CreateNewFeedAndReadFeedByID:
    """Create a new feed and read feed by ID."""

    def __init__(
            self,
            feed_provider: SimpleFeedInterface
    ):
        """Init."""
        self.feed_provider = feed_provider

    async def __call__(self, feed: Feed) -> Optional[FeedDetail]:
        """
        Create a new feed.

        Args:
            feed: A Feed DTO.

        Returns:
            A FeedDetail DTO
        """
        feed_detail = FeedDetail(**feed.dict())
        feed_detail.id = await CreateNewFeed(
            feed_provider=self.feed_provider)(feed=feed)
        return feed_detail
