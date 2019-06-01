"""
    An repository manager used to manage warehouse objects stored in repository
    Author: Ajeet Singh
    Date: 05/31/2019
"""
from bipy.core.db import categories
from bipy.core.db.repository.objects import WarehouseDatabase, WarehouseSchema
from bipy.core.db.repository.objects import WarehouseTable, WarehouseColumn


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

    def get_schema(self, param, database=None):
        """ Returns an instance of `WarehouseSchema` class stored in database based on
            id or name. If database parameter is passed, it will return schemas
            available under that database only

            Args:
                param(int/str): An Id or name of the schema
                database(WarehouseDatabase): An instance of WarehouseDatabase class
        """
        if database is None:
            if isinstance(param, int):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.id == param).first()
            elif isinstance(param, str):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.name == param).first()
        else:
            if isinstance(param, int):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.id == param \
                                and WarehouseSchema.database_id == database.id).first()
            elif isinstance(param, str):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.name == param \
                               and WarehouseSchema.database_id == database.id).first()
        return None

    def get_all_schemas(self, database=None):
        """ Returns instances of all schemas available under an database passed as
            parameter else returns all schemas available under all databases

            Args:
                database(WarehouseDatabase): An instance of WarehouseDatabase class
        """
        if database is None:
            return self.__session.query(WarehouseSchema).all()

        return self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.database_id == database.id).all()

    def get_all_schema_names(self, database=None):
        """Returns names of all available schemas under an passed database or
            all schemas under all database

            Args:
                database(WarehouseDatabase): An instance of WarehouseDatabase class
        """
        _names = []
        _schemas = None
        if database is None:
            _schemas = self.__session.query(WarehouseSchema).all()
        else:
            _schemas = self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.database_id == database.id).all()
        for sch in _schemas:
            _names.append(sch.name)
        return _names

    def get_table(self, param, schema=None):
        """ Returns an instance of `WarehouseTable` available under an schema passed
            as parameter else returns instances of all tables matching the table name or
            id passed as parameter(param)

            Args:
                param(int/str): An id or name of the table
                schema(WarehouseSchema): An instance of schema class
        """
        if schema is None:
            if isinstance(param, str):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param).first()
            elif isinstance(param, int):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.id == param).first()
        else:
            if isinstance(param, str):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param and\
                                WarehouseTable.schema_id == schema.id)\
                        .first()
            elif isinstance(param, int):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param\
                                and WarehouseTable.schema_id == schema.id)\
                        .first()
        return None

    def get_all_tables(self, schema=None):
        """ Returns instances of all tables available under an schema passed
            as parameter else returns all tables from all schemas and
            databases

            Args:
                schema(WarehouseSchema): An instance of schema class
        """
        if schema is None:
            return self.__session.query(WarehouseTable).all()

        return self.__session.query(WarehouseTable)\
                    .filter(WarehouseTable.schema_id == schema.id).all()

    def get_all_table_names(self, schema=None):
        """ Returns name of all tables available under an schema passed as
            parameter else return name of all tables available under all
            schemas and databases

            Args:
                schema(WarehouseSchema): An instance of schema class
        """
        _tables = None
        _names = []
        if schema is None:
            _tables = self.__session.query(WarehouseTable).all()
        else:
            _tables = self.__session.query(WarehouseTable)\
                    .filter(WarehouseTable.schema_id == schema.id).all()
        for tab in _tables:
            _names.append(tab.name)

        return _names

    def get_column(self, table=None, schema=None, db=None):
        pass
