from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cinema Review Authenticity Platform"
    env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/cinema_review"
    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/1"
    celery_result_backend: str = "redis://redis:6379/2"
    enable_scraped_sources: bool = False
    openai_api_key: str = ""
    tmdb_api_key: str = ""
    omdb_api_key: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "cinema-review-bot/1.0"
    allow_cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
