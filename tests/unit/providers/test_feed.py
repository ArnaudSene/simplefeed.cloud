"""Unit tests for feed."""
from unittest import IsolatedAsyncioTestCase

from databases import Database
from sqlalchemy import insert, create_engine

from src.domains.feed import FeedDetail, FeedModel, Base
from src.providers.feed import SimpleFeedProvider


class TestSimpleFeedP(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Create database for testing."""
        self.database_url = 'sqlite:///./tests/db_test.db'
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

        test 1: expected same data for id: 0
        test 2: data is instance of FeedDetail
        """
        expected = {
            'id': 1,
            "origin": "fake.origin_0",
            "event": "A fake event 0",
            "description": "This is a fake description 0",
        }
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feeds = await provider.read_feeds()
            self.assertEqual(feeds[0].dict(), expected)
            self.assertIsInstance(feeds[0], FeedDetail)
            self.assertEqual(len(feeds), 5)

    async def test_read_feeds_result_is_empty_list(self):
        """
        Read feeds. (no data in database).

        test 1: expected an empty list
        """
        async with Database(self.database_url, force_rollback=True) as db:
            provider = SimpleFeedProvider()
            provider.database = db
            feeds = await provider.read_feeds()
            self.assertListEqual(feeds, [])

    async def test_read_mind_map_app(self):
        """
        Read an app by app id.

        test 1: expected same data for id: fake-app-0
        test 2: ata is instance of MindMapApp
        """
        feed_id = 1
        expected = {
            'id': 1,
            "origin": f"fake.origin_0",
            "event": f"A fake event 0",
            "description": f"This is a fake description 0",
        }
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feed = await provider.read_feed_by_id(feed_id=feed_id)
            self.assertEqual(feed.dict(), expected)
            self.assertIsInstance(feed, FeedDetail)

    async def test_read_mind_map_app_result_is_none(self):
        """
        Read feed by id.

        test 1: result is None with id not in database
        """
        feed_id = 999
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            provider = SimpleFeedProvider()
            provider.database = db
            feed = await provider.read_feed_by_id(feed_id=feed_id)
            self.assertIsNone(feed)

    async def test_create_feed(self):
        """
        Create a new feed.

        test 1: result is a key == 1
        """
        sample_feed = {
            "origin": f"fake.origin_0",
            "event": f"A fake event 0",
            "description": f"This is a fake description 0",
        }
        feed = FeedDetail(**sample_feed)
        async with Database(self.database_url, force_rollback=True) as db:
            provider = SimpleFeedProvider()
            provider.database = db
            key = await provider.create_feed(feed=feed)
            self.assertEqual(key, 1)

    # async def test_create_feed_raise_exception(self):
    #     """
    #     Create a new feed but id already exist in db.
    #
    #     test 1: raise FeedCreateError
    #     """
    #     sample_feed = {
    #         "id"
    #         "origin": f"fake.origin_0",
    #         "event": f"A fake event 0",
    #         "description": f"This is a fake description 0",
    #     }
    #     feed = FeedDetail(**sample_feed)
    #     async with Database(self.database_url, force_rollback=True) as db:
    #         await self.load_db(database=db)
    #         provider = SimpleFeedProvider()
    #         m.database = db
    #         with pytest.raises(FeedCreateError):
    #             await m.create_feed(mind_map_app=app)

