from typing import List, Optional
from pydantic import BaseModel

class Config(BaseModel):
    name: str
    data: str

class ConfigData(BaseModel):
    repo: Optional[dict]
    build: Optional[dict]
    config: List[Config]
