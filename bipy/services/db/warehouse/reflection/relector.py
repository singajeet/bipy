"""This module helps in getting the reflection of the Warehouse database and
will be used by the analysis engine to create and compile queries for
analysis.

Author: Ajeet Singh
Date: 06/22/2018
"""
from sqlalchemy import text, column, MetaData
from bipy.services.utils import Utility


class Reflector:
    """Class to explore database through reflection APIs
    """

    __connection_mgr = None
    __session = None
    __engine = None
    __metadata = None
    __INSTANCE = None
    __util = None
    __config = None

    def __new__(cls):
        if Reflector.__INSTANCE is None:
            Reflector.__INSTANCE = object.__new__(cls)
        return Reflector.__INSTANCE

    def __init__(self):
        self.__util = Utility()
        self.__config = self.__util.CONFIG
        self.__connection_mgr = self.__util.get_plugin(self.__config.PATH_CONNECTION_MANAGERS)
        self.__connection_mgr.connect(self.__config.URL_TEST_DB)
        self.__engine = self.__connection_mgr.get_engine()
        self.__session = self.__connection_mgr.ConnectedSession
        self.__metadata = MetaData(self.__engine)
        self.__metadata.reflect(bind=self.__engine)

    def get_table(self, table_name):
        """Returns an instance of the table that exists in the target
            warehouse

            Args:
                table_name (String): Name of the table available in warehouse
        """
        if self.__metadata is not None:
            table = self.__metadata.tables.get(table_name)
            if table is not None:
                return table
            else:
                raise ValueError("Provided table '%s' doesn't exist in the warehouse" % (table_name))
        else:
            raise ReferenceError("The referenced metadata is not available yet. \
                Please check the configuration file to make sure the path to the \
                warehouse is correct!")

    def get_columns_list(self, columns):
        """Returns an list of columns casted to `sqlalchemy.column` type

            Args:
                columns (String): A comma seperated list of column names
        """
        column_array = str(columns).split(',')
        column_list = []
        for col in column_array:
            col_obj = column(col)  # Wrap with sqlalchemy.column object
            column_list.append(col_obj)
        return column_list

    def get_where_conditon(self, condition_string):
        """returns an object of sqlalchemy.text for the given string condition

            Args:
                condition_string (String): An where condition provided in string form
        """
        return text(condition_string)

    def get_order_by_condition(self, order_by_string):
        """Returns an object of sqlalchemy.text for the given order by condition

            Args:
                order_by_string (strinng): An order by text string
        """
        return text(order_by_string)

    def prepare_query(self, table, columns=None, where_cond=None, order_by_cond=None):
        """Combines all parameters to prepare an SQL statement for execution
        This will return the statement only not the result set

            Args:
                table (sqlalchemy.table): An table object
                columns (List[sqlalchemy.column]): An list of columns
                where_cond (sqlalchemy.text): A where condition wrapped in text object
                order_by (sqlalchemy.text): An order by condition wrapped in text object
        """
        statement = table.select()

        if columns is not None:
            statement = statement.with_only_columns(columns)

        statement = statement.select_from(table)

        if where_cond is not None:
            statement = statement.where(where_cond)

        if order_by_cond is not None:
            statement = statement.order(order_by_cond)

        return statement

    def execute_statement(self, statement):
        """Executes the provided statement and returns back the result set

            Args:
                statement (sqlalchemy.select): An select statement
        """
        return self.__session.execute(statement)
