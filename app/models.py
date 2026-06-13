from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_slug = Column(String, index=True, nullable=False)
    autor = Column(String, nullable=False)
    email = Column(String, nullable=True)
    texto = Column(String, nullable=False)
    data_criacao = Column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo"))
    )