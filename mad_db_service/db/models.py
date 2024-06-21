from typing import Optional, List
from sqlmodel import SQLModel, Field


class MemesData(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(...)
    description: Optional[str] = Field(default="описание отсутствует")
    url: str = Field(...)


