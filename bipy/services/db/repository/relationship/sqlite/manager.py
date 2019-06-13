"""
    An repository manager used to manage warehouse objects stored in repository
    Author: Ajeet Singh
    Date: 05/31/2019
"""
from bipy.services.db import categories
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
                repo_mgr(RepositoryManager): Instance of
                                                RepositoryManager class

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
        LOGGER.debug("Adding schema '%s' to database '%s'"
                     % (schema.name if schema.name is not None else "Unknown",
                        db.name if db.name is not None else "Unknown"))
        db_exists = False
        db_obj = self.__repo_manager.get_database(db.name)
        if db_obj is not None and db_obj.__len__() != 0:
            db_exists = True

        schema_exists = False
        schema_obj = self.__repo_manager.get_schema(schema.name, db)
        if schema_obj is not None and schema_obj.__len__() != 0:
            schema_exists = True

        if not db_exists:
            LOGGER.debug("DB '%s' do not exist, creating DB in repository"
                         % (db.name if db.name is not None else "Unknown"))
            self.__repo_manager.save(db)

        if not schema_exists:
            LOGGER.debug("Schema '%s' do not exist, \
                         creating schema in repository"
                         % (schema.name if schema.name is not None
                            else "Unknown"))
            self.__repo_manager.save(schema)
        db.schemas.append(schema)
        self.__session.commit()
        LOGGER.debug("Schema added to database successfully!")

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
        LOGGER.debug("Adding table '%s' to schema '%s'"
                     % (table.name if table.name is not None else "Unknown",
                        schema.name if schema.name is not None else "Unknown"))
        schema_exists = False
        schema_obj = self.__repo_manager.get_schema(schema.name)

        if schema_obj is not None and schema_obj.__len__() != 0:
            schema_exists = True
        table_exists = False
        table_obj = self.__repo_manager.get_table(table.name, schema)
        if table_obj is not None and table_obj.__len__() != 0:
            table_exists = True
        if not schema_exists:
            LOGGER.debug("Schema '%s' does not exist, creating schema now"
                         % (schema.name if schema.none is not None
                            else "Unknown"))
            self.__repo_manager.save(schema)
        if not table_exists:
            LOGGER.debug("Table '%s' does not exist, creating table now"
                         % (table.name if table.none is not None
                             else "Unknown"))
            self.__repo_manager.save(table)
        schema.tables.append(table)
        self.__session.commit()
        LOGGER.debug("Table has been added to schema successfully!")

    def add_tables_to_schema(self, tables, schema):
        """ Add's a list of tables under the provided
            schema. It is similar to add_table_to_schema

            Args:
                tables(List): A list of table instances
                schema(WarehouseSchema): An instance of schema objects
        """
        for tab in tables:
            self.add_table_to_schema(tab, schema)

    def add_view_to_schema(self, view, schema):
        """ Add's an view to provided schema. It also saves the
            view and schema objects if not already saved

            Args:
                view(WarehouseView): An view object
                schema(WarehouseSchema): An schema object
        """
        LOGGER.debug("Adding view '%s' to schema '%s'"
                     % (view.name if view.name is not None else "Unknown",
                        schema.name if schema.name is not None else "Unknown"))
        schema_exists = False
        schema_obj = self.__repo_manager.get_schema(schema.name)
        if schema_obj is not None and schema_obj.__len__() != 0:
            schema_exists = True

        view_exists = False
        view_obj = self.__repo_manager.get_view(view.name, schema)
        if view_obj is not None and view_obj.__len__() != 0:
            view_exists = True
        if not schema_exists:
            LOGGER.debug("Schema '%s' does not exist, creating schema now"
                         % (schema.name if schema.none is not None
                            else "Unknown"))
            self.__repo_manager.save(schema)
        if not view_exists:
            LOGGER.debug("View '%s' does not exist, creating view now"
                         % (view.name if view.none is not None
                             else "Unknown"))
            self.__repo_manager.save(view)
        schema.views.append(view)
        self.__session.commit()
        LOGGER.debug("View has been added to schema successfully!")

    def add_views_to_schema(self, views, schema):
        """ Add's a list of views under the provided
            schema. It is similar to add_view_to_schema

            Args:
                views(List): A list of view instances
                schema(WarehouseSchema): An instance of schema objects
        """
        for vw in views:
            self.add_view_to_schema(vw, schema)

    def add_column_to_table(self, column, table):
        """ Add's an column instance to the table provided as
            parameter

            Args:
                column(WarehouseColumn): An instance of column
                table(WarehouseTable): An instance of table
        """
        LOGGER.debug("Adding column '%s' to table '%s'" %
                     (column.name if column.name is not None else "Unknown",
                      table.name if table.name is not None else "Unknown"))
        table_exists = False
        table_obj = self.__repo_manager.get_table(table.name)
        if table_obj is not None and table_obj.__len__() != 0:
            table_exists = True
        column_exists = False
        column_obj = self.__repo_manager.get_column(column.name, table)
        if column_obj is not None and column_obj.__len__() != 0:
            column_exists = True
        if not table_exists:
            LOGGER.debug("Table '%s' does not exists, creating new table" %
                         (table.name if table.name is not None
                          else "Unknown"))
            self.__repo_manager.save(table)
        if not column_exists:
            LOGGER.debug("Column '%s' does not exist, creating new column"
                         % (column.name if column.name is not None
                            else "Unknown"))
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
        LOGGER.debug("Removing schema '%s' from DB '%s'" %
                     (schema.name if schema.none is not None else "Unknown",
                      db.name if db.name is not None else "Unknown"))
        for sch in db.schemas:
            if sch.id == schema.id:
                db.schemas.remove(sch)
                self.__session.commit()
                LOGGER.debug("Schema removed successfully from DB")
        return schema

    def remove_table_from_schema(self, table, schema):
        """ Removes the provided table from list of tables available
            under passed schema

            Args:
                table(WarehouseTable): Table object that needs to be
                    removed
                schema(WarehouseSchema): Schema object that contains
                        the tables
        """
        LOGGER.debug("Removing table '%s' from schema '%s'" %
                     (table.name if table.name is not None else "Unknown",
                      schema.name if schema.name is not None else "Unknown"))
        for tb in schema.tables:
            if tb.id == table.id:
                schema.tables.remove(tb)
                self.__session.commit()
                LOGGER.debug("Table removed from schema successfully!")
        return table

    def remove_column_from_table(self, column, table):
        """ Removes the column from the table. Both table and column are passed
            as argument to this method

            Args:
                column(WarehouseColumn): Column that needs to be removed
                table(WarehouseTable): Table from where column needs to
                                        be removed
        """
        LOGGER.debug("Removing column '%s' from table '%s'" %
                     (column.name if column.name is not None else "Unknown",
                      table.name if table.name is not None else "Unknown"))
        for col in table.columns:
            if col.id == column.id:
                table.columns.remove(col)
                self.__session.commit()
                LOGGER.debug("Column removed successfully from table!")

    def remove_schemas_from_db(self, schemas, db):
        """ Same as `remove_schema_from_db` but removes all schemas
            passed as list

            Args:
                schemas(List): List of schemas
                db(WarehouseDatabase): Instance of DB from where schemas
                                         will be removed
        """
        for sch in schemas:
            self.remove_schema_from_db(sch, db)

    def remove_tables_from_schema(self, tables, schema):
        """ Same as `remove_table_from_schema` but removes all tables
            passed as list

            Args:
                tables(List): List of tables
                schema(WarehouseSchema): Instance of schema from where
                                            tables will be removed
        """
        for tab in tables:
            self.remove_table_from_schema(tab, schema)

    def remove_columns_from_schema(self, columns, table):
        """ Same as `remove_column_from_table` but removes all
            columns passed as list

            Args:
                colums(List): List of columns that needs to be removed
                table(WarehouseTable): Table from where columns will be removed
        """
        for col in columns:
            self.remove_column_from_table(col, table)
