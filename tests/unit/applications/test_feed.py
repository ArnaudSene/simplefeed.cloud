"""Unit tests for feed."""
from unittest import TestCase, IsolatedAsyncioTestCase

from databases import Database
from sqlalchemy import create_engine, insert

from src.applications.feed import ReadFeeds, ReadFeedById, CreateNewFeed, \
    CreateNewFeedAndReadFeedByID
from src.domains.feed import Base, FeedModel, Feed
from src.providers.feed import SimpleFeedProvider


class TestFeedApplications(IsolatedAsyncioTestCase):

    database_url = 'sqlite:///./tests/db_test.db'

    async def asyncSetUp(self):
        """Create database for testing."""
        engine = create_engine(self.database_url)
        Base.metadata.create_all(engine)

    @staticmethod
    async def load_db(database: Database):
        """Load data in db for testing."""
        values = [{
            "origin": f"fake.origin_{i}",
            "event": f"A fake event {i}",
            "description": f"This is a fake description {i}",
        } for i in range(5)]
        query = insert(FeedModel)
        await database.execute_many(query=query, values=values)

    async def test_read_feeds(self):
        """
        Read feeds.

        test 1: result is a list with 5 feeds
        test 2: result has structure has expected
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feeds = await ReadFeeds(feed_provider=provider)()
            expected = {
                "origin": f"fake.origin_0",
                "event": f"A fake event 0",
                "description": f"This is a fake description 0",
                "id": 1
            }
            self.assertEqual(len(feeds), 5)
            self.assertEqual(feeds[0].dict(), expected)

    async def test_read_feeds_empty_list(self):
        """
        Read feeds but result is an empty list.

        test 1: result is an empty list
        """
        async with Database(self.database_url, force_rollback=True) as db:
            provider = SimpleFeedProvider()
            provider.database = db
            feeds = await ReadFeeds(feed_provider=provider)()
            self.assertListEqual(feeds, [])

    async def test_read_feed_by_id(self):
        """
        Read feed by id.

        test 1: result has structure has expected
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feed_id = 1
            feed = await ReadFeedById(feed_provider=provider)(feed_id=feed_id)
            expected = {
                "origin": f"fake.origin_0",
                "event": f"A fake event 0",
                "description": f"This is a fake description 0",
                "id": 1
            }
            self.assertEqual(feed.dict(), expected)

    async def test_read_feed_by_id_result_is_none(self):
        """
        Read feed by id with invalid feed_id.

        test 1: result is None
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feed_id = 999
            feed = await ReadFeedById(feed_provider=provider)(feed_id=feed_id)
            self.assertIsNone(feed)

    async def test_create_new_feed(self):
        """
        Create a new feed.

        test 1: result is a feed_id
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feed_id_expected = 6
            feed = Feed(
                origin="fake_origin",
                event="fake_event",
                description="fake_description"
            )
            feed_id = await CreateNewFeed(feed_provider=provider)(feed=feed)
            self.assertEqual(feed_id, feed_id_expected)

    async def test_create_new_feed_and_read_feed_by_id(self):
        """
        Create a new feed and read feed by ID.

        test 1: result is a feed struct has expected
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feed_expected = {
                "origin": "fake_origin",
                "event": "fake_event",
                "description": "fake_description",
                "id": 6
            }
            feed = Feed(
                origin="fake_origin",
                event="fake_event",
                description="fake_description"
            )
            feed_result = await CreateNewFeedAndReadFeedByID(
                feed_provider=provider)(feed=feed)
            self.assertEqual(feed_result.dict(), feed_expected)

