"""
    An repository manager used to manage warehouse objects stored in repository
    Author: Ajeet Singh
    Date: 05/31/2019
"""
from bipy.core.db import categories
from bipy.core.db.repository.objects import WarehouseDatabase, WarehouseSchema


class RepositoryManager(categories.SQLite):
    """
        An manager class to manage repo objects
    """

    __instance = None
    __connection = None
    __session = None

    def __new__(cls):
        """ Method to create singleton instance
        """
        if RepositoryManager.__instance is None:
            RepositoryManager.__instance = object.__new__(cls)
        return RepositoryManager.__instance

    def __init__(self):
        """ Default constructor
        """
        categories.SQLite.__init__(self)

    def connect(self, conn):
        """ Init connection with meta repo db

            Args:
                conn(ConnectionManager): An connection instance to DB

        """
        self.__connection = conn
        self.__session = self.__connection.get_session()

    def save(self, repo_obj):
        """ Saves the repo object to database

            Args:
                repo_obj(AbstractWarehouseObject): An instance of warehouse
                object
        """
        self.__session.add(repo_obj)
        self.__session.commit()

    def update(self):
        """ Updates all objects associated with current session
        """
        self.__session.commit()

    def delete(self, repo_obj):
        """Delete an repo object from db

            Args:
                repo_obj(AbstractWarehouseObject): An instance of warehouse
                item
        """
        repo_obj.delete()
        self.__session.commit()

    def get_database(self, param):
        """ Returns an instance of `WarehouseDatabase` class

            Args:
                param (int/str): An id or name of the database
        """
        if type(param) == int:
            return self.__session.query(WarehouseDatabase).filter(WarehouseDatabase.id == param).first()
        elif type(param) == str:
            return self.__session.query(WarehouseDatabase).filter(WarehouseDatabase.name == param).first()
