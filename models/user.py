#!/usr/bin/python3
"""
User Class

The user class defines every instance of budgtr users
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import hashlib


class User(BaseModel, Base):
    """
    User
    
    Inherits the id, created_at and updated_at
    from the BaseModel.
    takes:
     - email
     - firstname
     - lastname
     - password
    """
    __tablename__ = "users"

    email = Column(String(100),
                   nullable=False,
                   unique=True)
    firstname = Column(String(100),
                       nullable=True)
    lastname = Column(String(100),
                      nullable=True)
    password = Column(String(100),
                      nullable=False,
                      unique=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        hasher = hashlib.md5()
        hasher.update(self.password.encode('utf-8'))
        self.password = hasher.hexdigest()
    
    def check_password(self, password):
        """checks if the entered password is the correct password"""
        hasher = hashlib.md5()
        hasher.update(password.encode('utf-8'))
        password = hasher.hexdigest()

        if self.password == password:
            return True
        else:
            return False
