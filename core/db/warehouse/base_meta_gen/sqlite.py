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
from bipy.core.db.repository.objects import WarehouseView, WarehouseMaterializedView


class MetaGenerator:
    """ This class will deal with the core logic of generating metadata using
    an SQLite objects passed as list to the function parameters. This class will
    not browse database to get list of objects but instead an list of each DB 
    object will be passed to respective function. Further, browser object will be
    passed to get the value of additional attributes. This will help in keeping GUI,
    DB Browsing, Meta generation and saving objects in repository loosely coupled.
    This class will be an singleton class
    """

    __instance = None

    def __new__(cls, val):
        if MetaGenerator.__instance is None:
            MetaGenerator.__instance = object.__new__(cls)
        MetaGenerator.__instance.val = val
        return MetaGenerator.__instance

    def __init__(self):
        pass

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

    def generate_schemas_meta(self, schema_list, database_id):
        """Generates an list of repository schema object and fill in the
            required info

            Args:
                schema_list (List): An list of schema names
                database_id (Integer): An database id field from repository
                                        object of type - WarehouseDatabase
        """
        schemas = []
        for schema in schema_list:
            schema_obj = WarehouseSchema()
            schema_obj.name = schema
            schema_obj.database_id = database_id
            schemas.extend(schema_obj)
        return schemas

    def generate_tables_meta(self, table_list, schema_id, browser):
        """Generates an list of tables as repository objects

            Args:
                table_list (Dict): A list of table names
                schema_id (string): A uniue id of schema from repository
                                    object - WarehouseSchema
                browser (Browser): An database browser object
        """
        tables = []
        for table in table_list:
            table_obj = WarehouseTable()
            table_obj.name = table
            columns = browser.get_columns(table)
            table_obj.number_of_columns = columns.__len__()
            for col in columns:
                if col['type'].__str__().__eq__('INTEGER'):
                    table_obj.contains_numeric_column = True
            table_obj.schema_id = schema_id
            tables.extend(table_obj)
        return tables


    def generate_views_meta(self, view_list, schema_id, browser):
        """Generates an list of views as repository objects

            Args:
                view_list (List): A list of view names
                schema_id (string): A unique id of schema from repository
                                        object - WarehouseSchema
                browser (Browser): An database browser object
        """
        views = []
        for view in view_list:
            view_obj = WarehouseView()
            view_obj.name = view
            columns = browser.get_columns(view)
            view_obj.number_of_columns = columns.__len__()
            for col in columns:
                if col['type'].__str__().__eq__('INTEGER'):
                    view_obj.contains_numeric_column = True
            view_obj.schema_id = schema_id
            views.extend(view)
        return views

    def generate_mviews_meta(self, mview_list):
        pass

    def generate_procedures_meta(self, proc_list):
        pass

    def generate_functions_meta(self, func_list):
        pass

    def generate_columns_meta(self, column_list):
        pass
