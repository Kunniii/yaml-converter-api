from pydantic import BaseModel


class PostData(BaseModel):
    data: str