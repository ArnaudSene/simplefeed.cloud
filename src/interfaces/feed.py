"""Feature: feed."""

import abc
from typing import List, Optional

from src.domains.feed import FeedDetail, Feed


class SimpleFeedInterface(abc.ABC):
    """Abstract class for SimpleFeed."""

    @abc.abstractmethod
    async def read_feeds(self) -> List[FeedDetail]:
        """
        Read feeds.

        Returns:
            A list of FeedDetail DTO
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def read_feed_by_id(self, feed_id: int) -> Optional[FeedDetail]:
        """
        Read feed by id.

        Args:
            feed_id: A feed id

        Returns:
            A FeedDetail DTO or None
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def create_feed(self, feed: Feed) -> int:
        """
        Create a new feed.

        Args:
            feed: A Feed DTO.

        Returns:
            A key id
        """
        raise NotImplementedError
