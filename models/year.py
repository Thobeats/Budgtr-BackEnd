#!/usr/bin/python3
"""
Year Class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Boolean
from datetime import datetime

class Year(BaseModel, Base):
    """Year Class
    
    Keyword arguments:
    year
    status
    """
    __tablename__ = "years"

    year = Column(String(100),
                  nullable=False,
                  default=datetime.now().year)
    status = Column(Boolean,
                    nullable=False,
                    default=1)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)