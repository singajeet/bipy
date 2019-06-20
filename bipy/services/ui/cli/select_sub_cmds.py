"""This module contains sub commands for selection of
    database objects from warehouse and same is stored
    in repository

    Author: Ajeet Singh
    Date: 20/06/2019
"""
from bipy.services.integration import selection


class SelectionSubCmds:
    """Singleton class for selection sub cmds"""

    __INSTANCE = None

    def __new__(cls):
        if SelectionSubCmds.__INSTANCE is None:
            SelectionSubCmds.__INSTANCE = object.__new__(cls)
        return SelectionSubCmds.__INSTANCE

    def select_database(self, sub_params, repo_conn):
        """Selects a database and store it in repo

            Args:
                sub_params (Array): An array of strings for parameters
                repo_conn (ConnectionManager): An connection to repo db
        """
        if sub_params.__len__() == 0:
            print("Missing required parameters. Use --help to get more information")
        elif sub_params.__len__() == 5:
            name = sub_params[0]
            db_type = sub_params[1]
            url = sub_params[2]
            user = sub_params[3]
            password = sub_params[4]
            result = selection.select_database(name, db_type, url, user, password)
            print("=>%s" % (result))
        elif sub_params.__len__() == 1 and str(sub_params[0]).lower() == '--help':
            print("")
            print("HELP:")
            print("-----")
            print("DATABASE command helps in selecting a db to be used in project")
            print("The DB is selected on the basis of details provided as params")
            print("USAGE: DATABASE name type conn_url username password")
            print("NOTE: All parameters are required for this command")
            print("")
        else:
            print("Invalid command or parameters. Use --help for more info")

    def select_schemas(self, sub_params, repo_conn):
        """Selects list of schemas under an database and stores it in repo

            Args:
                sub_params (Array): An array of strings for parameters
                repo_conn (ConnectionManager): An connection to repo db
        """
        if sub_params.__len__() == 0:
            print("Missing required parameters. Use --help to get more information")
        elif sub_params.__len__() == 2:
            schema_list = sub_params[0]
            database = sub_params[1]
            result = selection.select_schemas(schema_list, database, repo_conn)
            print("=>%s" % (result))
        elif sub_params.__len__() == 1 and str(sub_params[0]).lower() == '--help':
            print("")
            print("HELP:")
            print("-----")
            print("SCHEMAS command helps in selecting a list of schemas to be used in project")
            print("The schemas are selected on the basis of details provided as params")
            print("USAGE: SCHEMAS <sch1,sch2..> <database-name>")
            print("NOTE: All parameters are required for this command")
            print("")
        else:
            print("Invalid command or parameters. Use --help for more info")

    def select_tables(self, sub_params, repo_conn, wh_conn):
        """Selects list of tables under an schema and stores it in repo

            Args:
                sub_params (Array): An array of strings for parameters
                repo_conn (ConnectionManager): An connection to repo db
                wh_conn (ConnectionManager): An connection to warehouse
        """
        if sub_params.__len__() == 0:
            print("Missing required parameters. Use --help to get more information")
        elif sub_params.__len__() == 2:
            table_list = sub_params[0]
            schema = sub_params[1]
            result = selection.select_tables(table_list, schema, repo_conn, wh_conn)
            print("=>%s" % (result))
        elif sub_params.__len__() == 1 and str(sub_params[0]).lower() == '--help':
            print("")
            print("HELP:")
            print("-----")
            print("TABLES command helps in selecting a list of tables to be used in project")
            print("The tables are selected on the basis of details provided as params")
            print("USAGE: TABLES <tab1,tab2..> <schema-name>")
            print("NOTE: All parameters are required for this command")
            print("")
        else:
            print("Invalid command or parameters. Use --help for more info")

    def select_views(self, sub_params, repo_conn, wh_conn):
        """Selects list of views under an schema and stores it in repo

            Args:
                sub_params (Array): An array of strings for parameters
                repo_conn (ConnectionManager): An connection to repo db
                wh_conn (ConnectionManager): An connection to warehouse
        """
        if sub_params.__len__() == 0:
            print("Missing required parameters. Use --help to get more information")
        elif sub_params.__len__() == 2:
            view_list = sub_params[0]
            schema = sub_params[1]
            result = selection.select_views(view_list, schema, repo_conn, wh_conn)
            print("=>%s" % (result))
        elif sub_params.__len__() == 1 and str(sub_params[0]).lower() == '--help':
            print("")
            print("HELP:")
            print("-----")
            print("VIEWS command helps in selecting a list of views to be used in project")
            print("The views are selected on the basis of details provided as params")
            print("USAGE: VIEWS <view,view2..> <schema-name>")
            print("NOTE: All parameters are required for this command")
            print("")
        else:
            print("Invalid command or parameters. Use --help for more info")

    def select_columns(self, sub_params, repo_conn, wh_conn):
        """Selects list of columns under an table and stores it in repo

            Args:
                sub_params (Array): An array of strings for parameters
                repo_conn (ConnectionManager): An connection to repo db
                wh_conn (ConnectionManager): An connection to warehouse
        """
        if sub_params.__len__() == 0:
            print("Missing required parameters. Use --help to get more information")
        elif sub_params.__len__() == 2:
            column_list = sub_params[0]
            table = sub_params[1]
            result = selection.select_columns(column_list, table, repo_conn, wh_conn)
            print("=>%s" % (result))
        elif sub_params.__len__() == 1 and str(sub_params[0]).lower() == '--help':
            print("")
            print("HELP:")
            print("-----")
            print("COLUMNS command helps in selecting a list of columns to be used in project")
            print("The columns are selected on the basis of details provided as params")
            print("USAGE: COLUMNS <col1,col2..> <table-name>")
            print("NOTE: All parameters are required for this command")
            print("")
        else:
            print("Invalid command or parameters. Use --help for more info")
