"""
    An repository manager used to manage warehouse objects stored in repository
    Author: Ajeet Singh
    Date: 05/31/2019
"""
from bipy.core.db import categories
from bipy.core.db.repository.objects import WarehouseDatabase, WarehouseSchema
from bipy.core.db.repository.objects import WarehouseTable, WarehouseColumn
from bipy.core.db.repository.objects import WarehouseView
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
        LOGGER.debug("Saving repository object '%s' to repoistory database" % repo_obj.name)
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
                          database" % obj.name)
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
                         % repo_obj.name)
        except Exception:
            LOGGER.error("Unable to delete repository object '%s'" % repo_obj.name)
            raise

    def get_database(self, param):
        """ Returns an instance of `WarehouseDatabase` class

            Args:
                param (int/str): An id or name of the database
        """
        if isinstance(param, int):
            LOGGER.debug("Get request for WarehouseDatabase instance with id: '%d'" % param)
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.id == param).first()
        elif isinstance(param, str):
            LOGGER.debug("Get request for WarehouseDatabase instance with name: '%s'" % param)
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.name == param).first()
        LOGGER.warn("Incorreect datatype of parameter provided. Only 'int' and 'str' are accepted")
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
            LOGGER.debug("Adding '%s' database name to the list" % _db.name)
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
                              % (param, database.id))
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.id == param \
                                and WarehouseSchema.database_id == database.id).first()
            elif isinstance(param, str):
                LOGGER.debug("Request to get WarehouseSchema object with name: '%s' and database id: '%d'"\
                              % (param, database.id))
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
                      % database.id)
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
                          % database.id)
            _schemas = self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.database_id == database.id).all()
        for sch in _schemas:
            LOGGER.debug("Schema name '%s' added to the list" % sch.name)
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
                              % (param, schema.id))
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param and\
                                WarehouseTable.schema_id == schema.id)\
                        .first()
            elif isinstance(param, int):
                LOGGER.debug("Request to get table with id: '%d' under schema id: '%d'"\
                              % (param, schema.id))
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

        LOGGER.debug("Request to get all tables available under schema: '%d'" % schema.id)
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
                          % schema.id)
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
                          % (column, table.id))
            return self.__session.query(WarehouseColumn)\
                .filter(WarehouseColumn.table_id == table.id\
                        and WarehouseColumn.name == column)\
                .first()
        elif isinstance(column, int):
            LOGGER.debug("Request to get column with id: '%d' under table with id: '%id'"\
                          % (column, table.id))
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
                      % (table.id))
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
                      % (table.id))
        _columns = self.__session.query(WarehouseColumn)\
            .filter(WarehouseColumn.table_id == table.id)\
            .all()
        for col in _columns:
            LOGGER.debug("Adding column name '%s' to the list" % col.name)
            _names.append(col.name)
        LOGGER.debug("Returning all column names available under table with id: '%d'"\
                      % table.id)
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
                              % (param, schema.id))
                return self.__session.query(WarehouseView)\
                        .filter(WarehouseView.name == param\
                                and WarehouseView.schema_id == schema.id)\
                        .first()
            elif isinstance(param, int):
                LOGGER.debug("Request to get view with id: '%d' under schema id: '%d'"\
                              % (param, schema.id))
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

        LOGGER.debug("Request to get all views available under schema id: '%d'" % schema.id)
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
                          % schema.id)
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

    def add_schema_to_db(self, schema, db):
        """ Add an schema passed as argument to the db passed
            as well

            Args:
                schema(WarehouseSchema): An instance of schema
                db(WarehouseDatabase): An instance of db
        """
        db_exists = self.get_database(db.name)\
            .__len__() != 0
        schema_exists = self.get_schema(schema.name, db)\
            .__len__() != 0
        if not db_exists:
            self.save(db)
        if not schema_exists:
            self.save(schema)
        db.schemas.append(schema)
        self.__session.commit()

    def add_schemas_to_db(self, schemas, db):
        """ Same as add_schema_to_db but this adds an list of
            schemas to db

            Args:
                schemas(List): An list of schema objects
                db(WarehouseDatabase): An db object
        """
        for schema in schemas:
            self.add_schema_to_db(schema, db)

    def add_table_to_schema(self, table, schema):
        """ Add's an table to provided schema. It also saves the
            table and schema objects if not already saved

            Args:
                table(WarehouseTable): An table object
                schema(WarehouseSchema): An schema object
        """
        schema_exists = self.get_schema(schema.name)\
            .__len__() != 0
        table_exists = self.get_table(table.name, schema)\
            .__len__() != 0
        if not schema_exists:
            self.save(schema)
        if not table_exists:
            self.save(table)
        schema.tables.append(table)
        self.__session.commit()

    def add_tables_to_schema(self, tables, schema):
        """ Add's a list of tables under the provided
            schema. It is similar to add_table_to_schema

            Args:
                tables(List): A list of table instances
                schema(WarehouseSchema): An instance of schema objects
        """
        for tab in tables:
            self.add_table_to_schema(tab, schema)

    def add_column_to_table(self, column, table):
        """ Add's an column instance to the table provided as
            parameter

            Args:
                column(WarehouseColumn): An instance of column
                table(WarehouseTable): An instance of table
        """
        table_exists = self.get_table(table.name)\
            .__len__() != 0
        column_exists = self.get_column(column.name, table)\
            .__len__() != 0
        if not table_exists:
            self.save(table)
        if not column_exists:
            self.save(column)
        table.columns.append(column)
        self.__session.commit()

    def add_columns_to_table(self, columns, table):
        """ Add columns from provided list to table ppassed as
            argument

            Args:
                columns(List): A list of columns to be added to DB
                table(WarehouseTable): An instance of table class
        """
        for col in columns:
            self.add_column_to_table(col, table)

    def remove_schema_from_db(self, schema, db):
        """ Removes provided schema from list of schemas available
            under db passed as argument

            Args:
                schema(WarehouseSchema): Schema object to be removed
                table(WarehouseTable): Table containing the schema object
        """
        for sch in db.schemas:
            if sch.id == schema.id:
                db.schemas.remove(sch)

    def remove_table_from_schema(self, table, schema):
        """ Removes the provided table from list of tables available
            under passed schema

            Args:
                table(WarehouseTable): Table object that needs to be
                    removed
                schema(WarehouseSchema): Schema object that contains
                        the tables
        """
        for tb in schema.tables:
            if tb.id == table.id:
                schema.tables.remove(tb)

    def remove_column_from_table(self, column, table):
        """ Removes the column from the table. Both table and column are passed
            as argument to this method

            Args:
                column(WarehouseColumn): Column that needs to be removed
                table(WarehouseTable): Table from where column needs to be removed
        """
        for col in table.columns:
            if col.id == column.id:
                table.columns.remove(col)

    def remove_schemas_from_db(self, schemas, db):
        """ Same as `remove_schema_from_db` but removes all schemas passed as list

            Args:
                schemas(List): List of schemas
                db(WarehouseDatabase): Instance of DB from where schemas will be removed
        """
        for sch in schemas:
            self.remove_schema_from_db(sch, db)

    def remove_tables_from_schema(self, tables, schema):
        """ Same as `remove_table_from_schema` but removes all tables passed as list

            Args:
                tables(List): List of tables
                schema(WarehouseSchema): Instance of schema from where tables will be removed
        """
        for tab in tables:
            self.remove_table_from_schema(tab, schema)

    def remove_columns_from_schema(self, columns, table):
        """ Same as `remove_column_from_table` but removes all columns passed as list

            Args:
                colums(List): List of columns that needs to be removed
                table(WarehouseTable): Table from where columns will be removed
        """
        for col in columns:
            self.remove_column_from_table(col, table)
