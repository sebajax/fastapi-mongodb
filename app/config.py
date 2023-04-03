"""
core configuration for api
"""

from pydantic import BaseSettings, Field, Required


class Settings(BaseSettings):
    """
    class to represent the core settings for the api using Pydantic
    """
    # api libs env variables
    PROJECT_NAME: str = Field(default=Required, env="PROJECT_NAME")
    VERSION: str = "1.0.0"
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    ENV: str = Field(default=Required, env="ENV")
    # mongodb env variables
    MONGO_SERVER: str = Field(default=Required, env="MONGO_SERVER")
    MONGO_USER: str = Field(default=Required, env="MONGO_USER")
    MONGO_PASS: str = Field(default=Required, env="MONGO_PASS")
    MONGO_DB: str = Field(default=Required, env="MONGO_DB")
    MONGO_PORT: str = Field(default=Required, env="MONGO_PORT")


settings = Settings()
