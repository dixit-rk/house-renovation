from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/house_renovation"
    REDIS_URL: str = "redis://localhost:6379/0"
    GROQ_API_KEY: str = ""
    GROQ_VISION_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    DEBUG: bool = True
    STORAGE_UPLOAD_DIR: str = "storage/uploads"
    STORAGE_GENERATED_DIR: str = "storage/generated"
    STORAGE_REPORTS_DIR: str = "storage/reports"
    # Local Hugging Face image generation (no external API).
    HF_IMAGE_MODEL: str = "stabilityai/sd-turbo"
    IMAGE_MAX_SIZE: int = 512
    IMAGE_STEPS: int = 4
    IMAGE_STRENGTH: float = 0.6

    @property
    def upload_dir(self) -> Path:
        return BASE_DIR / self.STORAGE_UPLOAD_DIR

    @property
    def generated_dir(self) -> Path:
        return BASE_DIR / self.STORAGE_GENERATED_DIR

    @property
    def reports_dir(self) -> Path:
        return BASE_DIR / self.STORAGE_REPORTS_DIR


settings = Settings()
