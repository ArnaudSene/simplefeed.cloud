"""Unit test for Feed API."""
from unittest import IsolatedAsyncioTestCase

from databases import Database
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, insert

from main import app, DB_PROVIDER
from src.domains.feed import Base, FeedModel, FeedDetail


class TestSimpleFeedAPI(IsolatedAsyncioTestCase):
    """Unit Test for Feed API."""

    database_url = 'sqlite:///./tests/db_test.db'
    client = TestClient(app)

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
        } for i in range(1, 6)]
        query = insert(FeedModel)
        await database.execute_many(query=query, values=values)

    async def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers['content-type'], 'text/html; charset=utf-8')

    async def test_read_feeds(self):
        """
        Read feeds.

        test 1: Status code == 200
        test 2: Result has structure has expected
        """
        feed_details = [FeedDetail(
            origin=f"fake.origin_{i}",
            event=f"A fake event {i}",
            description=f"This is a fake description {i}",
            id=i).dict() for i in range(1, 6)]

        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            DB_PROVIDER.database = db
            response = self.client.get("/feeds")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), feed_details)

    async def test_read_feeds_empty_list(self):
        """
        Read feeds but get an empty list.

        test 1: Status code == 200
        test 2: Result is an empty list
        """
        feed_details = []

        async with Database(self.database_url, force_rollback=True) as db:
            DB_PROVIDER.database = db
            response = self.client.get("/feeds")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), feed_details)

    async def test_read_feed_by_id(self):
        """
        Read feed by id.

        test 1: Status code == 200
        test 2: Result has structure has expected
        """
        feed_details = FeedDetail(
            origin=f"fake.origin_1",
            event=f"A fake event 1",
            description=f"This is a fake description 1",
            id=1).dict()

        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            DB_PROVIDER.database = db
            response = self.client.get("/feed/1")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), feed_details)

    async def test_read_feed_by_id_invalid_feed_id(self):
        """
        Read feed with an invalid id.

        test 1: Status code == 200
        test 2: Result is None
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            DB_PROVIDER.database = db
            response = self.client.get("/feed/999")

            self.assertEqual(response.status_code, 200)
            self.assertIsNone(response.json())

    async def test_create_feed(self):
        """
        Create a new feed.

        test 1: Status code == 200
        test 2: Result has structure has expected
        """
        feed_details = FeedDetail(
            origin="fake.origin",
            event="A fake event",
            description="This is a fake description",
            id=6).dict()

        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            DB_PROVIDER.database = db
            response = self.client.post(
                "/feed/",
                json={
                    "origin": "fake.origin",
                    "event": "A fake event",
                    "description": "This is a fake description"
                }
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), feed_details)

    async def test_create_feed_invalid_body(self):
        """
        Create a new feed.

        test 1: Status code == 422
        test 2: Result has structure has expected
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            DB_PROVIDER.database = db
            response = self.client.post(
                "/feed/",
                json={
                    "origin": "fake.origin",
                    "event": "A fake event",
                }
            )

            self.assertEqual(response.status_code, 422)

    async def test_create_feed_invalid_url(self):
        """
        Create a new feed.

        test 1: Status code == 404
        test 2: Result has structure has expected
        """
        async with Database(self.database_url, force_rollback=True) as db:
            await self.load_db(database=db)
            DB_PROVIDER.database = db
            response = self.client.post(
                "/_invalid_feed/",
                json={
                    "origin": "fake.origin",
                    "event": "A fake event",
                    "description": "This is a fake description"
                }
            )

            self.assertEqual(response.status_code, 404)
