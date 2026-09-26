from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # .euv is the preferred configuration file.  Keep .env and OPENAI_* names
    # working so existing installations do not need to be changed at once.
    model_config = SettingsConfigDict(env_file=(".env", ".euv"), extra="ignore")
    llm_api_key: str = Field(
        default="", validation_alias=AliasChoices("LLM_API_KEY", "OPENAI_API_KEY")
    )
    llm_base_url: str = Field(
        default="https://api.openai.com/v1",
        validation_alias=AliasChoices("LLM_BASE_URL", "OPENAI_BASE_URL"),
    )
    llm_model: str = Field(
        default="gpt-4o-mini", validation_alias=AliasChoices("LLM_MODEL", "OPENAI_MODEL")
    )
    data_dir: Path = Path("data")
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    chunk_size: int = 900
    chunk_overlap: int = 120
    bkt_initial: float = 0.20
    bkt_guess: float = 0.20
    bkt_slip: float = 0.10
    bkt_learn: float = 0.15

    @property
    def chroma_dir(self) -> Path:
        return self.data_dir / "chroma"

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.data_dir / 'coursepilot.db'}"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    return settings
