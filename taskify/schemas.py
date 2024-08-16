from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    comments: Optional[List[str]] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
