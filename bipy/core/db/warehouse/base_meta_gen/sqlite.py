"""
    This module contains the functionality to generate database metadata and
    populate repository objects with the required information. The repository
    objects will become the base of the analysis services and all analytic
    objects (metrics, dimensions, etc) will be built on top of it. This module
    will specifically deal with the warehouse built using SQLite.

    Author: Ajeet Singh
    Date: 05/21/2019
"""
from bipy.core.db.repository.objects import WarehouseDatabase, WarehouseSchema
from bipy.core.db.repository.objects import WarehouseTable, WarehouseColumn
from bipy.core.db.repository.objects import WarehouseView
from bipy.core.db import categories



class MetaGenerator(categories.SQLite):
    """
        This class will deal with the core logic of generating metadata using
        an SQLite objects passed as list to the function parameters. This class will
        not browse database to get list of objects but instead an list of each DB
        object will be passed to respective function. Further, browser object will be
        passed to get the value of additional attributes. This will help in keeping GUI,
        DB Browsing, Meta generation and saving objects in repository loosely coupled.
        This class will be an singleton class.

	>>> from bipy.core.db.categories import SQLite

	>>> from bipy.core.constants import PATHS, URLS

	>>> from yapsy.PluginManager import PluginManager

    >>> manager = PluginManager(categories_filter={'SQLITE': SQLite})

	>>> manager.setPluginPlaces([PATHS.CONNECTION_MANAGERS])

    >>> manager.locatePlugins()

    >>> connections = manager.loadPlugins()

    >>> connections.__len__()
    1
    >>> connections[0].name
    'SQLite Connection Manager'

	>>> conn = connections[0].plugin_object

    >>> manager.setPluginPlaces([PATHS.BROWSERS])

    >>> manager.locatePlugins()

    >>> browsers = manager.loadPlugins()

    >>> browsers.__len__()
    1
    >>> browsers[0].name
    'SQLite Metadata Browser'
    >>> browser = browsers[0].plugin_object

    >>> conn.connect(URLS.TEST_DB)

    >>> browser.connect(conn)

    >>> browser.get_schemas()
    ['main']
    >>> browser.get_tables()
    []
    >>> manager.setPluginPlaces([PATHS.BASE_META_GEN])

	>>> manager.locatePlugins()

    >>> bmg = manager.loadPlugins()

    >>> bmg.__len__()
    1
    >>> bmg[0].name
    'SQLite MetaData Generator'
    >>> mg = bmg[0].plugin_object

    >>> db = mg.generate_database_meta("SQLITE", URLS.TEST_DB, "user", "pass")

    >>> db
    Warehouse [Name=None, Type=SQLITE]

	>>>
    """

    __instance = None

    def __new__(cls):
        """Singleton class implementation
        """
        if MetaGenerator.__instance is None:
            MetaGenerator.__instance = object.__new__(cls)
        return MetaGenerator.__instance

    def __init__(self):
        """Default constructor
        """
        categories.SQLite.__init__(self)

    def generate_database_meta(self, db_type, conn_str, username, password):
        """Generates an repository database object with the parameters passed

            Args:
                db_type (string): An type describing the database (SQLite, MySQL, etc)
                conn_str (string): connection string or url to database
                username (string): username to connect with DB
                password (string): password to connect with DB
        """
        database = WarehouseDatabase()
        database.db_type = db_type
        database.connection_string = conn_str
        database.username = username
        database.password = password
        return database

    def generate_schemas_meta(self, schema_list, database):
        """Generates an list of repository schema object and fill in the
            required info

            Args:
                schema_list (List): An list of schema names
                database (WarehouseDatabase): An database instance (WarehouseDatabase)
        """
        if database is None:
            raise ValueError("Database parameter should not be a None value")
        schemas = []
        for schema in schema_list:
            schema_obj = WarehouseSchema()
            schema_obj.name = schema
            #schema_obj.database_id = database.id
            database.schemas.append(schema_obj)
            schemas.append(schema_obj)
        return schemas

    def generate_tables_meta(self, table_list, schema, browser):
        """Generates an list of tables as repository objects

            Args:
                table_list (Dict): A list of table names
                schema (WarehouseSchema): A schema instance (WarehouseSchema)
                browser (Browser): An database browser object
        """
        if schema is None:
            raise ValueError("Schema parameter should not be a None value")
        if browser is None:
            raise ValueError("Browser parameter should not be a None value")
        tables = []
        for table in table_list:
            table_obj = WarehouseTable()
            table_obj.name = table
            columns = browser.get_columns(table)
            table_obj.number_of_columns = columns.__len__()
            for col in columns:
                if col['type'].__str__().__eq__('INTEGER'):
                    table_obj.contains_numeric_column = True
            #table_obj.schema_id = schema.id
            schema.tables.append(table_obj)
            tables.append(table_obj)
        return tables


    def generate_views_meta(self, view_list, schema, browser):
        """Generates an list of views as repository objects

            Args:
                view_list (List): A list of view names
                schema (WarehouseSchema): A schema instance (WarehouseSchema)
                browser (Browser): An database browser object
        """
        if schema is None:
            raise ValueError("Schema parameter should not be a None value")
        if browser is None:
            raise ValueError("Browser parameter should not be a None value")
        views = []
        for view in view_list:
            view_obj = WarehouseView()
            view_obj.name = view
            columns = browser.get_columns(view)
            view_obj.number_of_columns = columns.__len__()
            for col in columns:
                if col['type'].__str__().__eq__('INTEGER'):
                    view_obj.contains_numeric_column = True
            view_obj.schema_id = schema.id
            views.extend(view_obj)
        return views

    def generate_mviews_meta(self, mview_list, schema, browser):
        """Generates an list of Materialized View as repo objects
            **WARNING**: Materialized Views are not supported in SQLite
                         Please don't use this method
            Args:
                mview_list (List): A list of materialized view names
                schema (WarehouseSchema): A schema instance (WarehouseSchema)
                browser (Browser): An database browser instance
        """
        raise NotImplementedError("Materialized Views are not supported by SQLite")

    def generate_procedures_meta(self, proc_list, schema, browser):
        """Generates an list of Procedures as repo objects
            **WARNING**: Procedures are not supported in SQLite
                            Please don't use this method
            Args:
                 proc_list (List): A list of procedure names
                 schema (WarehouseSchema): A schema instance (WarehouseSchema)
                 browser (Browser): An database browser instance
        """
        raise NotImplementedError("Procedures are not supported by SQLite")

    def generate_functions_meta(self, func_list, schema, browser):
        """Generates an list of Functions as repo objects
            **WARNING**: Functions are not supported in SQLite
                            Please don't use this method
            Args:
                 func_list (List): A list of function names
                 schema (WarehouseSchema): A schema instance (WarehouseSchema)
                 browser (Browser): An database browser instance
        """
        raise NotImplementedError("Functions are not supported by SQLite")

    def generate_columns_meta(self, column_list, schema, table, browser):
        """Generates an list of columns as repo objects

            Args:
                 column_list (List): A list of procedure names
                 schema (WarehouseSchema): A schema instance (WarehouseSchema)
                 table (WarehouseTable): A table instance (WarehouseTable)
                 browser (Browser): An database browser instance
        """
        if schema is None:
            raise ValueError("Schema parameter should not be a None value")
        if browser is None:
            raise ValueError("Browser parameter should not be a None value")
        if table is None:
            raise ValueError("Table parameter should not be a None value")
        columns = []
        for column in column_list:
            col_obj = WarehouseColumn()
            col_obj.name = column
            col_obj.column_type = browser.get_column_type(table.name, column)
            pk_cols = browser.get_primary_key_columns(table.name)
            for pk in pk_cols:
                if pk.__eq__(column):
                    col_obj.is_primary_key = True
            if col_obj.column_type.__eq__('INTEGER'):
                col_obj.is_fact_candidate = True
            if col_obj.column_type.__ne__('INTEGER'):
                col_obj.is_dim_candidate = True
            col_obj.table_id = table.id
            columns.extend(col_obj)
        return columns


if __name__ == "__main__":
    import doctest
    doctest.testmod()
