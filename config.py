from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AdminLoginSchema(BaseModel):
    email: EmailStr
    password: str


class HTTPClient(BaseModel):
    base_url: HttpUrl
    timeout: int

    @property
    def url(self) -> str:
        return str(self.base_url)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
        extra="ignore",
    )
    admin_login_data: AdminLoginSchema
    http_client: HTTPClient


settings = Settings()
