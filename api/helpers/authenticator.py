#!/usr/bin/python3

from models.user import User
from models.engine.db import DB


class Authenticator:
    """
    The Authenticator Class communicates basically
    with the User Model.
    It checks and authenticates the user.
    """

    def __init__(self) -> None:
        self.__db = DB()

    def check(self, **kwargs) -> None:
        """checks if the user exist based on the provided info"""
        query = self.__db.auth_check(email=kwargs['email'], password=kwargs['password'])
        return query

    