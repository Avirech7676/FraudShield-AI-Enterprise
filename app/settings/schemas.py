from pydantic import BaseModel


class UserSettings(BaseModel):

    username: str

    role: str

    jwt_expiry_minutes: int


class SystemSettings(BaseModel):

    backend: bool

    mongodb: bool

    prediction_engine: bool

    model_version: str

    api_version: str

    groq: bool

    shap: bool


class HealthStatus(BaseModel):

    backend: bool

    mongodb: bool

    prediction_engine: bool

    groq: bool

    shap: bool