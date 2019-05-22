"""
 Database sspecific meta models classes and will be used in the database meta browser objects
 Author: Ajeet Singh
 Date: 05/08/2019
"""
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MetaModel(Base):
    """
        An metadata table mapped to SQLite's sqlite_master tabele to browse for DB objects
    """
    __tablename__ = 'sqlite_master'

    type = Column(String)
    name = Column(String, primary_key=True)
    tbl_name = Column(String)
    rootpage = Column(String)
    sql = Column(String)

    def __repr__(self):
        """
            Returns the representation of MetaModel class

            Returns:
                String: Object Name and Type
        """
        return "SQLiteMetaModel (Name=%s, Type=%s)" % (self.name, self.type)


class Browser:
    """
        An SQLite Metadata browser class implemented using sqlite_master table and
        SQLAlchemy's inspector function. It helps to browse through Tables, Views,
        etc available in an given database

        Args:
            connection (ConnectionManager): An instance of the ConnectionManager class
            pointing to the SQLite database

        Attributes:
            ConnectedSession (get_session): Stores the connected session to the database
            inspector (get_inspector): stores the inspector instance available
                                        though get_inspector function
    """

    ConnectedSession = None
    inspector = None
    __instance = None

    def __new__(cls, val):
        """The singleton constructor for this class
        """
        if Browser.__instance is None:
            Browser.__instance = object.__new__(cls)
        Browser.__instance.val = val
        return Browser.__instance

    def __init__(self, connection):
        """Default constructor of the SQLite's browser class

            Args:
                connection (ConnectionManager): An connection object to SQLite DB
        """
        self.ConnectedSession = connection.get_session()
        self.inspector = connection.get_inspector()

    def __repr__(self):
        """Returns string representation
        """
        return "SQLite browser instance"

    def get_tables(self):
        """Returns list of tables
        """
        return self.ConnectedSession.query(MetaModel).filter_by(type='table').all()

    def get_views(self):
        """Returns list of views
        """
        return self.ConnectedSession.query(MetaModel).filter_by(type='view').all()

    def get_columns(self, table_or_view_name):
        """
            Returns list of columns available in table or view

            Args:
                table_or_view_name (string): name of the table or view
        """
        return self.inspector.get_columns(table_or_view_name)

    def get_column_names(self, table_or_view_name):
        """
            Return list of column names

            Args:
                table_or_view_name (string): name of the table or view
        """
        column_names = []
        for col in self.inspector.get_columns(table_or_view_name):
            column_names.append(col['name'])
        return column_names

    def get_column_type(self, table_or_view_name, column_name):
        """
            Returns the type of column passed as arg of specific table
            passed as arg too

            Args:
                table_or_view_name (string): name of table or view
                column_name (string): name of the column
        """
        for col in self.inspector.get_columns(table_or_view_name):
            if col['name'] == column_name:
                return col['type']

        return None

    def get_primary_key_columns(self, table_or_view_name):
        """
            Returns an primary key column of the table passed as arg

            Args:
                table_or_view_name (string): name of table or view
        """
        pk_const = self.inspector.get_pk_constraint(table_or_view_name)
        return pk_const['constrained_columns']

    def get_primary_key_name(self, table_or_view_name):
        """
            Returns the name of the primary key column

            Args:
                table_or_view_name (string): name of the table or column
        """
        pk_const = self.inspector.get_pk_constraint(table_or_view_name)
        return pk_const['name']

    def get_table_options(self, table_name):
        """
            Returns options of a given table

            Args:
                table_name (string): name of the table
        """
        return self.inspector.get_table_options(table_name)

    def get_schema_names(self):
        """
            Returns list of schema names available
        """
        return self.inspector.get_schema_names()

    def get_foreign_keys(self, table_or_view_name):
        """
            Returns list of foreign keys available in the passed table

            Args:
                table_or_view_name (string): name of the table or view
        """
        return self.inspector.get_foreign_keys(table_or_view_name)

    def close(self):
        """
            Closes the connected session with the database
        """
        self.ConnectedSession.disconnect()
