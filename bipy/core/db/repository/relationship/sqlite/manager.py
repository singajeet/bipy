"""
    An repository manager used to manage warehouse objects stored in repository
    Author: Ajeet Singh
    Date: 05/31/2019
"""
from bipy.core.db import categories
from bipy.logging import logger


LOGGER = logger.get_logger(__name__)


class RepositoryRelationshipManager(categories.SQLite):
    """
        An manager class to manage repo objects
    """

    __instance = None
    __connection = None
    __session = None
    __repo_manager = None

    def __new__(cls):
        """ Method to create singleton instance
        """
        if RepositoryRelationshipManager.__instance is None:
            RepositoryRelationshipManager.__instance = object.__new__(cls)
        return RepositoryRelationshipManager.__instance

    def __init__(self):
        """ Default constructor
        """
        LOGGER.debug("RepositoryRelationshipManager instance created")
        categories.SQLite.__init__(self)

    def connect(self, conn, repo_mgr):
        """ Init connection with meta repo db

            Args:
                conn(ConnectionManager): An connection instance to DB
                repo_mgr(RepositoryManager): Instance of RepositoryManager class

        """
        LOGGER.debug("Connecting to database...")
        self.__connection = conn
        self.__session = self.__connection.get_session()
        self.__repo_manager = repo_mgr
        LOGGER.debug("Connected to database successfully")

    def add_schema_to_db(self, schema, db):
        """ Add an schema passed as argument to the db passed
            as well

            Args:
                schema(WarehouseSchema): An instance of schema
                db(WarehouseDatabase): An instance of db
        """
        db_exists = False
        db_obj = self.__repo_manager.get_database(db.name)
        if db_obj != None and db_obj.__len__() != 0:
            db_exists = True
        schema_exists = False
        schema_obj = self.__repo_manager.get_schema(schema.name, db)
        if schema_obj != None and schema_obj.__len__() != 0:
            schema_exists = True
        if not db_exists:
            self.__repo_manager.save(db)
        if not schema_exists:
            self.__repo_manager.save(schema)
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
        schema_exists = self.__repo_manager.get_schema(schema.name)\
            .__len__() != 0
        table_exists = self.__repo_manager.get_table(table.name, schema)\
            .__len__() != 0
        if not schema_exists:
            self.__repo_manager.save(schema)
        if not table_exists:
            self.__repo_manager.save(table)
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
        table_exists = self.__repo_manager.get_table(table.name)\
            .__len__() != 0
        column_exists = self.__repo_manager.get_column(column.name, table)\
            .__len__() != 0
        if not table_exists:
            self.__repo_manager.save(table)
        if not column_exists:
            self.__repo_manager.save(column)
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
                self.__session.commit()

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
                self.__session.commit()

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
                self.__session.commit()

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
