#!/usr/bin/python3
"""
Database Class

This class classifies the database model
- The database model use the SQLAlchemy library
"""

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, MetaData
from models.user import User
from models.year import Year
from models.month import Month
from models.otp import Otp
from models.base_model import Base
from dotenv import load_dotenv
from os import getenv
from flask import abort, request, jsonify


classes = {
    "user" : User,
    "month" : Month,
    "year" : Year,
    "otp" : Otp
}


class DB:
    """ Interacts with the Database """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialises a new database Instance    
        """
        load_dotenv()
        user = getenv("DB_USER")
        pwd = getenv("DB_PASSWORD")
        host = getenv("DB_HOST")
        db = getenv("DB_DATABASE")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user,pwd,host,db))

    def start_engine(self):
        """
        Starts the DB Engine
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        try:
            self.__session.commit()
            return True
        except Exception as e:
            print(e)
            self.__session.rollback()
            self.__session.flush()
            return False


    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, obj, id):
        """Gets an instance of a class by the id"""
        object_instance = self.__session.query(obj).get(id)
        return object_instance
    
    def auth_check(self, **kwargs):
        """tries to authenticate the user"""
        #self.start_engine()
        check = self.__session.query(User).filter(User.email == kwargs['email'],
                                          User.password == kwargs['password'])
    
    def all(self, obj=None):
        """Gets all instances of a particular class or all classes"""
        all_dicts = {}
        if obj is not None:
            if classes.get(obj):
                cls = classes[obj]
                all_objs = self.__session.query(cls).all()
                for __obj in all_objs:
                    key = "{}.{}".format(__obj.__class__.__name__, __obj.id)
                    all_dicts[key] = __obj
                return all_dicts
            else:
                return {}
        else:
            for cls in classes.values():
                all_objs = self.__session.query(cls).all()
                for __obj in all_objs:
                    key = "{}.{}".format(__obj.__class__.__name__, __obj.id)
                    all_dicts[key] = __obj
            return all_dicts
        
    def get_user_by_email(self, email):
        """Checks if a user with the email exists"""
        email_check = self.__session.query(User).filter(User.email == email).first()
        if email_check is not None:
            return email_check
        else:
            return None
        