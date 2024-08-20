from pydantic import BaseModel, Field
from datetime import datetime

class Video(BaseModel):
    name: str
    slug: str
    duration: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)