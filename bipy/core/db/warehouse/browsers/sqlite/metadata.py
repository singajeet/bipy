"""
 Database sspecific meta models classes and will be used in the database meta browser objects
 Author: Ajeet Singh
 Date: 05/08/2019
"""
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from bipy.core.db import categories
from bipy.logging import logger


LOGGER = logger.get_logger(__name__)
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


class Browser(categories.SQLite):
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

	>>> from bipy.core.db.categories import SQLite

        >>> from yapsy.PluginManager import PluginManager

        >>> from bipy.core.constants import PATHS, URLS

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
        ['CUSTOMER_MASTER', 'PRODUCT_MASTER', 'SALES_DETAILS', 'sqlite_sequence', 'warehouse_privileges', 'warehouse_roles', 'warehouse_roles_privileges', 'warehouse_users', 'warehouse_users_roles']
        >>>

    """

    ConnectedSession = None
    inspector = None
    __instance = None

    def __new__(cls):
        """The singleton constructor for this class
        """
        if Browser.__instance is None:
            Browser.__instance = object.__new__(cls)
        return Browser.__instance

    def __init__(self):
        """Default constructor of the SQLite's browser class
        """
        LOGGER.debug("Init SQLite Browser instance")
        categories.SQLite.__init__(self)

    def connect(self, connection):
        """Connects the browser to an database using connection passed as param

            Args:
                connection (ConnectionManager): An connection object to SQLite DB
        """
        self.ConnectedSession = connection.get_session()
        self.inspector = connection.get_inspector()
        LOGGER.debug("SQLite Browser connected to database successfully")

    def __repr__(self):
        """Returns string representation
        """
        return "SQLite browser instance"

    def get_schemas(self):
        """Returns list of schemas
        """
        return self.inspector.get_schema_names()

    def get_tables(self, schema=None):
        """Returns list of tables
        """
        return self.inspector.get_table_names(schema)

    def get_views(self, schema=None):
        """Returns list of views
        """
        return self.inspector.get_view_names(schema)

    def get_view_definition(self, schema=None):
        """Returns the SQL query used to create view
        """
        return self.inspector.get_view_definition(schema)

    def get_columns(self, table_name):
        """
            Returns list of columns available as dict object of a given table

            Args:
                table_name (string): name of the table
        """
        return self.inspector.get_columns(table_name)

    def get_column_names(self, table_name):
        """
            Return list of column names

            Args:
                table_name (string): name of the table
        """
        LOGGER.debug("Preparing to get column names for table: %s" % (table_name))
        column_names = []
        for col in self.inspector.get_columns(table_name):
            column_names.append(col['name'])
            LOGGER.debug("Column '%s' added to columns list" % (col['name']))
        LOGGER.debug("Columns list compiled and will be returned now")
        return column_names

    def get_column_type(self, table_name, column_name):
        """
            Returns the type of column, passed as arg of specific table
            passed as arg too

            Args:
                table_name (string): name of the table
                column_name (string): name of the column
        """
        LOGGER.debug("Preparing to get datatype of column '%s' in table '%s'"\
                      % (column_name, table_name))
        for col in self.inspector.get_columns(table_name):
            if col['name'] == column_name:
                LOGGER.debug("Column '%s' found in the respective table"\
                              % (column_name))
                col_str = str(col['type'])
                if col_str.find("(", 0) >= 0:
                    index = col_str.index("(", 0)
                    LOGGER.debug("'%s' will be returned as datatype for column '%s'"\
                                  % (col_str[0:index], column_name))
                    return col_str[0:index]
                LOGGER.debug("'%s' will be returned as datatype for column '%s'"\
                              % (col_str, column_name))
                return col_str
        return None

    def get_primary_key_columns(self, table_name):
        """
            Returns all columns available as primary key of the table passed as arg

            Args:
                table_name (string): name of the table
        """
        pk_const = self.inspector.get_pk_constraint(table_name)
        return pk_const['constrained_columns']

    def get_primary_key_name(self, table_name):
        """
            Returns the name of the primary key (i.e., name of PK constraint)

            Args:
                table_name (string): name of the table
        """
        pk_const = self.inspector.get_pk_constraint(table_name)
        return pk_const['name']

    def get_table_options(self, table_name):
        """
            Returns options of a given table

            Args:
                table_name (string): name of the table
        """
        return self.inspector.get_table_options(table_name)

    def get_foreign_keys(self, table_name):
        """
            Returns list of foreign keys as dict objects of a given table

            Args:
                table_name (string): name of the table
        """
        return self.inspector.get_foreign_keys(table_name)

    def close(self):
        """
            Closes the connected session with the database
        """
        self.ConnectedSession.close()
        LOGGER.debug("SQLite browser session has been closed")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
