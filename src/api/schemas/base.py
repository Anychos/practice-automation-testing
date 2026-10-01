from pydantic import BaseModel, ConfigDict


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BaseRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
