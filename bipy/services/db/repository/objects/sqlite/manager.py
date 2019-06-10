"""
    An repository manager used to manage warehouse objects stored in repository
    Author: Ajeet Singh
    Date: 05/31/2019
"""
from bipy.core.db import categories
from bipy.core.db.repository.meta_objects import WarehouseDatabase, WarehouseSchema
from bipy.core.db.repository.meta_objects import WarehouseTable, WarehouseColumn
from bipy.core.db.repository.meta_objects import WarehouseView
from bipy.logging import logger


LOGGER = logger.get_logger(__name__)


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
        LOGGER.debug("RepositoryManager instance created")
        categories.SQLite.__init__(self)

    def connect(self, conn):
        """ Init connection with meta repo db

            Args:
                conn(ConnectionManager): An connection instance to DB

        """
        LOGGER.debug("Connecting to database...")
        self.__connection = conn
        self.__session = self.__connection.get_session()
        LOGGER.debug("Connected to database successfully")

    def save(self, repo_obj):
        """ Saves the repo object to database

            Args:
                repo_obj(AbstractWarehouseObject): An instance of warehouse
                object
        """
        LOGGER.debug("Saving repository object '%s' to repository database" % \
                     (repo_obj.name if repo_obj.name is not None else "Unknown"))
        self.__session.add(repo_obj)
        self.__session.commit()
        LOGGER.debug("Repository object saved successfully")

    def save_all(self, repo_objs):
        """ Save all repo objects passed as list

            Args:
                repo_objs(List): An list of `AbstractWarehouseObject` objects
        """
        for obj in repo_objs:
            LOGGER.debug("Saving repository object instance '%s' from list to repository\
                          database" % (obj.name if obj.name is not None else "Unknown"))
        self.__session.add_all(repo_objs)
        self.__session.commit()
        LOGGER.debug("All repository object instances have bee saved successfully")

    def update(self):
        """ Updates all objects associated with current session
        """
        self.__session.commit()
        LOGGER.debug("All changes pending under current session have been updated")

    def delete(self, repo_obj):
        """Delete an repo object from db

            Args:
                repo_obj(AbstractWarehouseObject): An instance of warehouse
                item
        """
        try:
            repo_obj.delete()
            self.__session.commit()
            LOGGER.debug("Repository object '%s' have been deleted from repository" \
                         % (repo_obj.name if repo_obj.name is not None else "Unknown"))
        except Exception:
            LOGGER.error("Unable to delete repository object '%s'" % \
                         (repo_obj.name if repo_obj.name is not None else "Unknown"))
            raise

    def get_database(self, param):
        """ Returns an instance of `WarehouseDatabase` class

            Args:
                param (int/str): An id or name of the database
        """
        if isinstance(param, int):
            LOGGER.debug("Get request for WarehouseDatabase instance with id: '%d'" \
                         % param)
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.id == param).first()
        elif isinstance(param, str):
            LOGGER.debug("Get request for WarehouseDatabase instance with name: '%s'" \
                         % param)
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.name == param).first()
        LOGGER.warn("Incorrect datatype of parameter provided. Only 'int' and 'str' are accepted")
        return None

    def get_all_databases(self):
        """ Returns an list of all `WarehouseDatabase` objects
        """
        LOGGER.debug("Request to get all instances of WarehouseDatabase")
        return self.__session.query(WarehouseDatabase).all()

    def get_database_names(self):
        """ Returns an list of names of all databases
        """
        _names = []
        LOGGER.debug("Request to get names of all WarehouseDatabase objects")
        dbs = self.__session.query(WarehouseDatabase).all()
        for _db in dbs:
            LOGGER.debug("Adding '%s' database name to the list" \
                         % (_db.name if _db.name is not None else "Unknown"))
            _names.append(_db.name)
        LOGGER.debug("Returning the WarehouseDatabase names list")
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
                LOGGER.debug("Request to get WarehouseSchema object with id: '%d'" % param)
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.id == param).first()
            elif isinstance(param, str):
                LOGGER.debug("Request to get WarehouseSchema object with name: '%s'" % param)
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.name == param).first()
        else:
            if isinstance(param, int):
                LOGGER.debug("Request to get WarehouseSchema object with id: '%d' and database id: '%d'"\
                              % (param, \
                                 database.id if database.id is not None else -1))
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.id == param \
                                and WarehouseSchema.database_id == database.id).first()
            elif isinstance(param, str):
                LOGGER.debug("Request to get WarehouseSchema object with name: '%s' and database id: '%d'"\
                              % (param, \
                                 database.id if database.id is not None else -1))
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.name == param \
                               and WarehouseSchema.database_id == database.id).first()
        LOGGER.warn("Incorrect datatype of parameter provided. Only 'int' and 'str' are allowed")
        return None

    def get_all_schemas(self, database=None):
        """ Returns instances of all schemas available under an database passed as
            parameter else returns all schemas available under all databases

            Args:
                database(WarehouseDatabase): An instance of WarehouseDatabase class
        """
        if database is None:
            LOGGER.debug("Request to get all schemas available")
            return self.__session.query(WarehouseSchema).all()

        LOGGER.debug("Request to get all schemas available under database with id: '%d'"\
                      % database.id if database.id is not None else -1)
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
            LOGGER.debug("Request to get all schema names available")
            _schemas = self.__session.query(WarehouseSchema).all()
        else:
            LOGGER.debug("Request to get all schema names available under database id: '%d'"\
                          % database.id if database.id is not None else -1)
            _schemas = self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.database_id == database.id).all()
        for sch in _schemas:
            LOGGER.debug("Schema name '%s' added to the list" % (sch.name \
                         if sch.name is not None else "Unknown"))
            _names.append(sch.name)
        LOGGER.debug("Returning back list of schema names")
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
                LOGGER.debug("Request to get table with name: '%s'" % param)
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param).first()
            elif isinstance(param, int):
                LOGGER.debug("Request to get table with id: '%d'" % param)
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.id == param).first()
        else:
            if isinstance(param, str):
                LOGGER.debug("Request to get table with name: '%s' under schema id: '%d'"\
                              % (param, schema.id if schema.id is not None else -1))
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param and\
                                WarehouseTable.schema_id == schema.id)\
                        .first()
            elif isinstance(param, int):
                LOGGER.debug("Request to get table with id: '%d' under schema id: '%d'"\
                              % (param, schema.id if schema.id is not None else -1))
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.id == param\
                                and WarehouseTable.schema_id == schema.id)\
                        .first()
        LOGGER.debug("Incorrect datatype passed for parameter. Only 'int' and 'str' are accepted")
        return None

    def get_all_tables(self, schema=None):
        """ Returns instances of all tables available under an schema passed
            as parameter else returns all tables from all schemas and
            databases

            Args:
                schema(WarehouseSchema): An instance of schema class
        """
        if schema is None:
            LOGGER.debug("Request to get all tables available")
            return self.__session.query(WarehouseTable).all()

        LOGGER.debug("Request to get all tables available under schema: '%d'" \
                     % schema.id if schema.id is not None else -1)
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
            LOGGER.debug("Request to get all table names available")
            _tables = self.__session.query(WarehouseTable).all()
        else:
            LOGGER.debug("Request to get all table names available under schema id: '%d'"\
                          % schema.id if schema.id is not None else -1)
            _tables = self.__session.query(WarehouseTable)\
                    .filter(WarehouseTable.schema_id == schema.id).all()
        for tab in _tables:
            LOGGER.debug("Adding table name '%s' to the list" % tab.name)
            _names.append(tab.name)

        LOGGER.debug("Returning the list of table names available")
        return _names

    def get_column(self, column, table):
        """ Returns an instance of `WarehouseColumn` under an table
            passed as argument to this method

            Args:
                column(int/str): Name of the column or id
                table(WarehouseTable): An instance of table
        """
        if isinstance(column, str):
            LOGGER.debug("Request to get column with name: '%s' under table with id: '%d'"\
                          % (column, table.id if table.id is not None else -1))
            return self.__session.query(WarehouseColumn)\
                .filter(WarehouseColumn.table_id == table.id\
                        and WarehouseColumn.name == column)\
                .first()
        elif isinstance(column, int):
            LOGGER.debug("Request to get column with id: '%d' under table with id: '%id'"\
                          % (column, table.id if table.id is not None else -1))
            return self.__session.query(WarehouseColumn)\
                .filter(WarehouseColumn.id == column and\
                        WarehouseColumn.table_id == table.id)\
                .first()
        LOGGER.warn("Incorrect datatype provided as parameter. Only 'int' and 'str' are accepted")
        return None

    def get_all_columns(self, table):
        """ Returns instance list of all columns available
            under an table passed as argument

            Args:
                table(WarehouseTable): An instance of table
        """
        LOGGER.debug("Request to get all columns available under table with id: '%d'"\
                      % (table.id if table.id is not None else -1))
        return self.__session.query(WarehouseColumn)\
            .filter(WarehouseColumn.table_id == table.id)\
            .all()

    def get_all_column_names(self, table):
        """ Returns list of column names available
            under an table passed as argument

            Args:
                table(WarehouseTable): An instance of table
        """
        _names = []
        LOGGER.debug("Request to get all column names available under table with id: '%d'"\
                      % (table.id if table.id is not None else -1))
        _columns = self.__session.query(WarehouseColumn)\
            .filter(WarehouseColumn.table_id == table.id)\
            .all()
        for col in _columns:
            LOGGER.debug("Adding column name '%s' to the list" % \
                         (col.name if col.name is not None else "Unknown"))
            _names.append(col.name)
        LOGGER.debug("Returning all column names available under table with id: '%d'"\
                      % table.id if table.id is not None else -1)
        return _names

    def get_view(self, param, schema=None):
        """ Returns an instance of WarehoueView available
            under an schema passed as parameter

            Args:
                param(int/str): Id or name of the view
                schema(WarehouseSchema): An instance of the WarehouseSchema
        """
        if schema is None:
            if isinstance(param, str):
                LOGGER.debug("Request to get view with name: '%s'" % param)
                return self.__session.query(WarehouseView)\
                        .filter(WarehouseView.name == param).first()
            elif isinstance(param, int):
                LOGGER.debug("request to get view with id: '%d'" % param)
                return self.__session.query(WarehouseView)\
                        .filter(WarehouseView.id == param).first()
        else:
            if isinstance(param, str):
                LOGGER.debug("Request to get view with name: '%s' under schema id: '%d'"\
                              % (param, schema.id if schema.id is not None else -1))
                return self.__session.query(WarehouseView)\
                        .filter(WarehouseView.name == param\
                                and WarehouseView.schema_id == schema.id)\
                        .first()
            elif isinstance(param, int):
                LOGGER.debug("Request to get view with id: '%d' under schema id: '%d'"\
                              % (param, schema.id if schema.id is not None else -1))
                return self.__session.query(WarehouseView)\
                        .filter(WarehouseView.id == param and\
                                WarehouseView.schema_id == schema.id).first()
        LOGGER.debug("Incorrect datatype passed for parameter. \
                     Only 'int' and 'str' datatypes are allowed for parameter")
        return None

    def get_all_views(self, schema=None):
        """ Returns instances of all views available under an schema passed as
            parameter

            Args:
                schema(WarehouseSchema): An instance of warehouse schema object
        """
        if schema is None:
            LOGGER.debug("Request to get all views available in database")
            return self.__session.query(WarehouseView).all()

        LOGGER.debug("Request to get all views available under schema id: '%d'" % \
                     schema.id if schema.id is not None else -1)
        return self.__session.query(WarehouseView)\
                .filter(WarehouseView.schema_id == schema.id).all()

    def get_all_view_names(self, schema=None):
        """ Returns name of all available views under an schema passed as
            parameter

            Args:
                schema(WarehouseSchema): An instance of warehouse schema
        """
        _views = None
        _names = []
        if schema is None:
            LOGGER.debug("Request to get all view names available")
            _views = self.__session.query(WarehouseView).all()
        else:
            LOGGER.debug("Request to get all view names available under schema id: '%d'"\
                          % schema.id if schema.id is not None else -1)
            _views = self.__session.query(WarehouseView)\
                    .filter(WarehouseView.schema_id == schema.id).all()
        for vw in _views:
            LOGGER.debug("Adding view name '%s' to the list" % vw.name)
            _names.append(vw.name)

        LOGGER.debug("Returning the list of view names available")
        return _names

    def get_materialized_view(self, param, schema=None):
        """ Returns the MV instance matching the name or id passed as parameter.
            If schema is passed, it will lookup MVs under that schema only
            **WARNING**: SQLite doesn't support MVs

            Args:
                param(int/str): Id or name of the MV
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Materialized Views")
        raise NotImplementedError("SQLite does not support Materialized Views")

    def get_all_materialized_view(self, schema=None):
        """ Returns all MV instance available in the database.
            If schema is passed, it will lookup MVs under that schema only
            **WARNING**: SQLite doesn't support MVs

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Materialized Views")
        raise NotImplementedError("SQLite does not support Materialized Views")

    def get_all_materialized_view_names(self, schema=None):
        """ Returns list of names of all MV instance available in the database.
            If schema is passed, it will lookup MVs under that schema only
            **WARNING**: SQLite doesn't support MVs

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Materialized Views")
        raise NotImplementedError("SQLite does not support Materialized Views")

    def get_package(self, param, schema=None):
        """ Returns the package instance matching the name or id passed as parameter.
            If schema is passed, it will lookup Packages under that schema only
            **WARNING**: SQLite doesn't support Packages

            Args:
                param(int/str): Id or name of the package
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Packages")
        raise NotImplementedError("SQLite does not support Packages")

    def get_all_package(self, schema=None):
        """ Returns all package instances available in the database.
            If schema is passed, it will lookup Packages under that schema only
            **WARNING**: SQLite doesn't support Packages

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Packages")
        raise NotImplementedError("SQLite does not support Packages")

    def get_all_package_names(self, schema=None):
        """ Returns list of names of all package instance available in the database.
            If schema is passed, it will lookup Packages under that schema only
            **WARNING**: SQLite doesn't support Packages

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Packages")
        raise NotImplementedError("SQLite does not support Packages")

    def get_procedure(self, param, schema=None):
        """ Returns the procedure instance matching the name or id passed as parameter.
            If schema is passed, it will lookup Procedures under that schema only
            **WARNING**: SQLite doesn't support Procedures

            Args:
                param(int/str): Id or name of the procedure
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Procedures")
        raise NotImplementedError("SQLite does not support Procedures")

    def get_all_procedure(self, schema=None):
        """ Returns all procedure instances available in the database.
            If schema is passed, it will lookup Procedures under that schema only
            **WARNING**: SQLite doesn't support Procedure

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Procedures")
        raise NotImplementedError("SQLite does not support Procedures")

    def get_all_procedure_names(self, schema=None):
        """ Returns list of names of all procedure instance available in the database.
            If schema is passed, it will lookup Procedures under that schema only
            **WARNING**: SQLite doesn't support Procedures

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Procedures")
        raise NotImplementedError("SQLite does not support Procedures")

    def get_function(self, param, schema=None):
        """ Returns the function instance matching the name or id passed as parameter.
            If schema is passed, it will lookup Function under that schema only
            **WARNING**: SQLite doesn't support functions

            Args:
                param(int/str): Id or name of the function
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support Functions")
        raise NotImplementedError("SQLite does not support Functions")

    def get_all_function(self, schema=None):
        """ Returns all function instances available in the database.
            If schema is passed, it will lookup functions under that schema only
            **WARNING**: SQLite doesn't support functions

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support functions")
        raise NotImplementedError("SQLite does not support functions")

    def get_all_function_names(self, schema=None):
        """ Returns list of names of all function instance available in the database.
            If schema is passed, it will lookup function under that schema only
            **WARNING**: SQLite doesn't support functions

            Args:
                schema(WarehouseSchema): Instance of the warehouse schema
        """
        LOGGER.error("SQLite does not support functions")
        raise NotImplementedError("SQLite does not support functions")
