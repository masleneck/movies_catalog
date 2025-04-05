
from datetime import date
from pydantic import BaseModel, ConfigDict


class MovieCreate(BaseModel):
    title: str
    description: str = ""
    release_date: date | None = None
    duration: int | None = None

class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    release_date: date | None
    duration: int | None

    model_config = ConfigDict(from_attributes=True)