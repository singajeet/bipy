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

    def save_all(self, repo_objs):
        """ Save all repo objects passed as list

            Args:
                repo_objs(List): An list of `AbstractWarehouseObject` objects
        """
        self.__session.add_all(repo_objs)
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
        if isinstance(param, int):
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.id == param).first()
        elif isinstance(param, str):
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.name == param).first()
        return None

    def get_all_databases(self):
        """ Returns an list of all `WarehouseDatabase` objects
        """
        return self.__session.query(WarehouseDatabase).all()

    def get_database_names(self):
        """ Returns an list of names of all databases
        """
        _names = []
        dbs = self.__session.query(WarehouseDatabase).all()
        for _db in dbs:
            _names.append(_db.name)
        return _names

    def get_schema(self, param):
        """ returns an instance of `WarehouseSchema` class stored in database

            Args:
                param(int/str): An Id or name of the schema
        """
        if isinstance(param, int):
            return self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.id == param).first()
        elif isinstance(param, str):
            return self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.name == param).first()
        return None
