#!/usr/bin/python3
"""OTP Model"""

from models.base_model import Base
from sqlalchemy import Column, String, CHAR, DateTime, Integer
from datetime import datetime


class Otp(Base):
    """OTP Model for emails and phone numbers"""
    __tablename__ = 'otps'
    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    otp_code = Column(String(60),
                  nullable=False,
                  unique=True)
    identifier = Column(String(60),
                        nullable=False)
    status = Column(CHAR,
                    nullable=False,
                    default='A')
    expire_time = Column(Integer,
                         nullable=True,
                         default=3)
    created_at = Column(DateTime,
                        default=datetime.now)
    updated_at = Column(DateTime,
                        default=datetime.now)