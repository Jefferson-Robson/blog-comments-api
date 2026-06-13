from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentCreate(BaseModel):
    post_slug: str
    autor: str
    email: Optional[str] = None
    texto: str


class CommentResponse(BaseModel):
    id: int
    post_slug: str
    autor: str
    texto: str
    data_criacao: datetime

    class Config:
        from_attributes = True