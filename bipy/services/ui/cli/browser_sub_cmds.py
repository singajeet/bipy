"""Contaiins all sub commands to be used by BROWSE mai command

    Author: Ajeet Singh
    Date: 6/19/2019
"""
from bipy.services.integration import browser


class BrowserSubCmds:
    """Contains all sub commands to be used under BROWSE main command
    """

    __INSTANCE = None

    def __new__(cls):
        if BrowserSubCmds.__INSTANCE is None:
            BrowserSubCmds.__INSTANCE = object.__new__(cls)
        return BrowserSubCmds.__INSTANCE

    def print_column_type(self, sub_params):
        """Print details of column type that exists under a given table

            Args:
                sub_params (Array): An array of string params. It should
                                    have a table & column name as of params
        """
        if sub_params.__len__() == 0:
            print("Missing table & column name parameter. Please use --help to get more info")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            if sub_params.__len__() == 2:
                print("============================== COLUMN TYPE ============================")
                table = sub_params[0]
                column = sub_params[1]
                column_type = browser.column_type(table, column)
                print("==>Table: %s, Column: %s, Type: %s" % (table, column, column_type))
                print("===================================================================")
            else:
                print("Missing column name param. Please use --help to get more info")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("Print column type details of an column under an provided table")
            print("USAGE: COLUMN-TYPE <table-name> <column-name>")
            print("NOTE: both parameters are mandatory")
            print("")

    def list_column_names(self, sub_params):
        """Print details of all column names that exists under a given table

            Args:
                sub_params (Array): An array of string params. It should
                                    have a table name as one of param
        """
        if sub_params.__len__() == 0:
            print("Missing table name parameter. Please use --help to get more info")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("============================== COLUMNS NAMES ============================")
            table = sub_params[0]
            columns = browser.column_names(table)
            for col in columns:
                print("==>%s" % (col))
            print("===================================================================")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("List all columns with details under an provided table")
            print("USAGE: COLUMN-NAMES <table-name>")
            print("NOTE: parameter <table-name> is mandatory")
            print("")

    def list_columns(self, sub_params):
        """Print details of all columns that exists under a given table

            Args:
                sub_params (Array): An array of string params. It should
                                    have a table name as one of param
        """
        if sub_params.__len__() == 0:
            print("Missing table name parameter. Please use --help to get more info")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("============================== COLUMNS ============================")
            table = sub_params[0]
            columns = browser.columns(table)
            for col in columns:
                print("==>%s" % (col))
            print("===================================================================")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("List all columns with details under an provided table")
            print("USAGE: COLUMNS <table-name>")
            print("NOTE: parameter <table-name> is mandatory")
            print("")

    def print_view_def(self, sub_params):
        """Print the definition of view passed as argument

            Args:
                sub_params (Array): An array of string params. Should
                                    have name of view as one of param
        """
        if sub_params.__len__() == 0:
            print("Missing View name paramete. Please type --help to get more information")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            view = sub_params[0]
            schema = None
            if sub_params.__len__() == 2:
                schema = sub_params[1]
            print("========================= VIEW DEF =============================")
            print(browser.view_definition(view, schema))
            print("================================================================")
        elif sub_params[0].lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("VIEW-DEF command displays the SQL definition of an view")
            print("USAGE: VIEW-DEF <view-name> [schema-name]")
            print("NOTE: The <view-name> is a mandatory parameter & [schema-name] is optional")
            print("")

    def list_views(self, sub_params):
        """List all available views under an schema in configured warehouse

            Args:
                sub_params (Array): An of string parameters. Can have name of schema as params
        """
        if sub_params.__len__() == 0:
            print("========================== VIEWS ==============================")
            views = browser.views(self._warehouse_conn)
            for vw in views:
                print("==>%s" % (vw))
            print("================================================================")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("========================== VIEWS ==============================")
            schema = sub_params[0]
            views = browser.views(self._warehouse_conn, schema)
            for vw in views:
                print("==>%s" % (vw))
            print("================================================================")
        elif sub_params[0] == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("VIEW sub command can be used with or without parameter")
            print("The parameter passed should be an name of schema which should exist in warehouse")
            print("USAGE: VIEW <schema name>")
            print("NOTE: If no schema is provided, views from all schemas will be listed")
            print("")
        else:
            print("========================== VIEWS ==============================")
            views = browser.views(self._warehouse_conn)
            for vw in views:
                print("==>%s" % (vw))
            print("================================================================")

    def list_tables(self, sub_params):
        """List all available tables available under an schema in configured warehouse

            Args:
                sub_params (Array): An array of string parameters. Can have name of schema as params
        """
        if sub_params.__len__() == 0:
            print("========================== TABLES ==============================")
            tables = browser.tables(self._warehouse_conn)
            for tbl in tables:
                print("==>%s" % (tbl))
            print("================================================================")
        elif sub_params[0].lower() != "--help" and sub_params[0] != "":
            print("========================== TABLES ==============================")
            schema = sub_params[0]
            tables = browser.tables(self._warehouse_conn, schema)
            for tbl in tables:
                print("==>%s" % (tbl))
            print("================================================================")
        elif sub_params[0] == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("TABLE sub command can be used with or without parameter")
            print("The parameter passed should be an name of schema which should exist in warehouse")
            print("USAGE: TABLE <schema name>")
            print("NOTE: If no schema is provided, tables from all schemas will be listed")
            print("")
        else:
            print("========================== TABLES ==============================")
            tables = browser.tables(self._warehouse_conn)
            for tbl in tables:
                print("==>%s" % (tbl))
            print("================================================================")

    def list_schemas(self, sub_params):
        """List all available schemas  in the configured warehouse database

            Args:
                sub_params (Array): An array of string parameters
        """
        if sub_params.__len__() == 0:
            print("====================== SCHEMAS ==========================")
            schemas = browser.schemas(self._warehouse_conn)
            for schema in schemas:
                print("==>%s" % (schema))
            print("=========================================================")
        elif str(sub_params[0]).lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("List all available schemas in the configured warehouse database")
            print("No parameters are required to run this command")
            print("")
        else:
            print("ERROR: Command executed with invalid arguments. Please --help to get more information")

    def connect(self, params):
        """Connects to either warehouse or repo based on params passed

            Args:
                params (Array): An array of string parameters
        """
        if params.__len__() == 0:
            self._warehouse_conn = browser.connect()
        elif str(params[0]).lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("Connects to an Warehouse database configured in the system")
            print("No parameters are required to run this command")
            print("")
