"""simplefeed.cloud API."""
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.applications.feed import ReadFeeds, ReadFeedById, \
    CreateNewFeedAndReadFeedByID
from src.domains.feed import FeedDetail, FeedCreateError, Feed
from src.providers.feed import SimpleFeedProvider

# Define provider for dependency injection
DB_PROVIDER = SimpleFeedProvider()

# Define jinja template directory
templates = Jinja2Templates(directory="templates")

tags_metadata = [
    {
        "name": "simplefeed.cloud",
        "description": "simplefeed.cloud API",
        "externalDocs": {
            "description": "simplefeed.cloud API docs",
            "url": "https://127.0.0.1",
        },
    },
]

description = """
This API aims to do something but what ???.
"""
app = FastAPI(
    title="simplefeed.cloud API",
    description=description,
    version="0.0.1",
    terms_of_service="https://127.0.0.1/terms/",
    contact={
        "name": "Arnaud SENE",
        "url": "https://127.0.0.1/contact/",
        "email": "arnaud.sene@halia.ca",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """root html."""
    feeds = await ReadFeeds(feed_provider=DB_PROVIDER)()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "feeds": feeds,
        }
    )


@app.get("/feeds", response_model=List[FeedDetail], tags=["items"])
async def read_feeds() -> List[FeedDetail]:
    """Read feeds."""
    return await ReadFeeds(feed_provider=DB_PROVIDER)()


@app.get("/feed/{feed_id}", response_model=FeedDetail, tags=["items"])
async def read_feed_by_id(feed_id: int) -> FeedDetail:
    """Read feed by id."""
    return await ReadFeedById(feed_provider=DB_PROVIDER)(feed_id=feed_id)


@app.post("/feed/", response_model=FeedDetail, tags=["items"])
async def create_feed(feed: Feed) -> FeedDetail:
    """Create a new feed."""
    try:
        return await CreateNewFeedAndReadFeedByID(
            feed_provider=DB_PROVIDER)(feed=feed)

    except FeedCreateError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc))
