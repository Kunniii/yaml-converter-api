from typing import List
from pydantic import BaseModel

class Config(BaseModel):
    name: str
    data: str

class ConfigData(BaseModel):
    config: List[Config]