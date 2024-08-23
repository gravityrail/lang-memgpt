from __future__ import annotations

from functools import lru_cache

import langsmith
from langchain_core.runnables import RunnableConfig
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

from lang_memgpt import _schemas as schemas
from lang_memgpt import _settings as settings

_DEFAULT_DELAY = 60  # seconds


def get_vector_store(configurable: dict):
    return QdrantVectorStore.construct_instance(
        client_options={
            "url": configurable["qdrant_url"],
            "api_key": configurable["qdrant_api_key"]
        },
        collection_name=configurable["qdrant_collection_name"],
        embedding=get_embeddings(),
    )


@langsmith.traceable
def ensure_configurable(config: RunnableConfig) -> schemas.GraphConfig:
    """Merge the user-provided config with default values."""
    configurable = config.get("configurable", {})
    return {
        **configurable,
        **schemas.GraphConfig(
            api_key=configurable.get("api_key", settings.SETTINGS.api_key),
            delay=configurable.get("delay", _DEFAULT_DELAY),
            model=configurable.get("model", settings.SETTINGS.model),
            provider=configurable.get(
                "provider", settings.SETTINGS.provider
            ),
            qdrant_url=configurable.get("qdrant_url", settings.SETTINGS.qdrant_url),
            qdrant_api_key=configurable.get(
                "qdrant_api_key", settings.SETTINGS.qdrant_api_key
            ),
            qdrant_collection_name=configurable.get(
                "qdrant_collection_name", settings.SETTINGS.qdrant_collection_name
            ),
            thread_id=configurable.get("thread_id", settings.SETTINGS.thread_id),
            user_id=configurable.get("user_id", settings.SETTINGS.user_id),
        ),
    }


@lru_cache
def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")  # 1536 dims


__all__ = ["ensure_configurable"]
