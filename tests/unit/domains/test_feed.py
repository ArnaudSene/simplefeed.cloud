"""Unit tests for feed."""
from unittest import TestCase

from src.domains.feed import Feed, FeedDetail


class TestFeedDomains(TestCase):

    def test_feed(self):
        feed_data = {
            "origin": "fake_origin",
            "event": "fake_event",
            "description": "fake_description",
        }
        feed = Feed(**feed_data)
        self.assertEqual(feed.dict(), feed_data)

    def test_feed_detail(self):
        feed_detail_data = {
            "origin": "fake_origin",
            "event": "fake_event",
            "description": "fake_description",
            "id": 1
        }
        feed_detail = FeedDetail(**feed_detail_data)
        self.assertEqual(feed_detail.dict(), feed_detail_data)
