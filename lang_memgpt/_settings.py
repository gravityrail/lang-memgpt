from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    qdrant_url: str = os.environ.get("QDRANT_URL")
    qdrant_api_key: str = os.environ.get("QDRANT_API_KEY")
    qdrant_collection_name: str = os.environ.get("QDRANT_COLLECTION_NAME")
    model: str = "gpt-4o"
    provider: str = "openai"
    api_key: str = os.environ.get("OPENAI_API_KEY")
    thread_id: str = "1"
    user_id: str = ""


SETTINGS = Settings()
