import logging

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from main import app


logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("Starting cache in-memory backend")
    FastAPICache.init(InMemoryBackend(), prefix="api-cache")
