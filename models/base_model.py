#!/usr/bin/python3
"""
Base Model

This is the Parent Class
"""
from datetime import datetime
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4


Base = declarative_base()

class BaseModel:
    """BaseModel
    
    Keyword arguments:
    id - Id value of the model instance
    created_at - Timestamp of the model instance creation
    update_at - Timestamp of the model instance update
    """
    id = Column(String(60),
                primary_key=True,
                nullable=False)
    created_at = Column(DateTime,
                        default=datetime.now)
    updated_at = Column(DateTime,
                        default=datetime.now)

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialise a new class
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, time)
                elif key != "__class__":
                    setattr(self, key, value)
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
            if "id" not in kwargs:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    
    def save(self) -> bool:
        from models import storage

        """Save the database session"""
        self.updated_at = datetime.now()
        storage.new(self)
        response = storage.save()
        return response
    
