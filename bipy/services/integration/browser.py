"""Browser commands to be used by various interfaces
    like CLI, Web, etc

    Author: Ajeet Singh
    Date: 06/17/2019
"""
import hug
from bipy.services.utils import Utility


def connect():
    """Connects to an browser interface and returns
        the connection
    """
    util = Utility()
    config = util.CONFIG
    conns = util.get_plugin(config.PATH_CONNECTION_MANAGERS)
    conns.connect(config.URL_TEST_DB)
    return conns


def _browser():
    """Returns an instance of Browser plugin"""
    util = Utility()
    config = util.CONFIG
    browser = util.get_plugin(config.PATH_BROWSER)
    return browser


@hug.cli()
@hug.get()
def schemas(conn=None):
    """Returns instance of schemas in warehouse

        Args:
            conn (ConnectionManager): connection to warehouse db
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_schemas()


@hug.cli()
@hug.get()
def tables(conn=None, schema=None):
    """Returns instance of tables in warehouse

        Args:
            conn (ConnectionManager): connection to warehouse db
            schema (String): Schema name from where tables needs to be listed
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_tables(schema)


@hug.cli()
@hug.get()
def views(conn=None, schema=None):
    """Returns instance of views in warehouse

        Args:
            conn (ConnectionManager): connection to warehouse db
            schema (String): Schema name from where views needs to be listed
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_views(schema)


@hug.cli()
@hug.get()
def view_definition(view, schema=None, conn=None):
    """Returns SQL query used for creating view. A ConnectionManager instance
        can be passed to this function, if it's not passed, this method tries
        to get the connection on its own

        Args:
            view (String): View mame
            schema (String): Schema name, by default it is None
            conn (ConnectionManager): ConnectionManager instance
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_view_definition(view, schema)


@hug.cli()
@hug.get(output=hug.output_format.text)
def columns(table, conn=None):
    """Returns a list of column dict objects with details of each column.
        It tries to get the connection itself if one is not passed

        Args:
            table (String): Name of the table
            conn (ConnectionManager): ConnectionManager instance
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_columns(table)


@hug.cli()
@hug.get()
def column_names(table, conn=None):
    """Returns a list of column names under an provided table.

        Args:
            table (String): Name of the table
            conn (ConnectionManager): ConnectionManager instance
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_column_names(table)


@hug.cli()
@hug.get()
def column_type(table, column, conn=None):
    """Returns an database type of an column available under provided
        table

        Args:
            table (String): Name of the table
            column (String): Name of the column
            conn (ConnectionManager): An instance of ConnectionManager
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_column_type(table, column)


@hug.cli()
@hug.get()
def pk_columns(table, conn=None):
    """Return column names which makes a primary key in the table

        Args:
            table (String): Name of the table
            conn (ConnectionString): An instance of ConnectionManager
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_primary_key_columns(table)


@hug.cli()
@hug.get()
def pk_name(table, conn=None):
    """Returns the name of primary key in the provided table

        Args:
            table (String): Name of the table
            conn (ConnectionString): An instance of ConnectionManager
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_primary_key_name(table)


@hug.cli()
@hug.get()
def table_options(table, conn=None):
    """Returns the options available for the provided table

        Args:
            table (String): Name of the table
            conn (ConnectionString): An instance of ConnectionManager
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_table_options(table)


@hug.cli()
@hug.get()
def fk_columns(table, conn=None):
    """Return column names which makes a foreign keys in the table

        Args:
            table (String): Name of the table
            conn (ConnectionString): An instance of ConnectionManager
    """
    if conn is None:
        conn = connect()
    br = _browser()
    br.connect(conn)
    return br.get_foreign_keys(table)


@hug.cli()
@hug.get()
def close(conn=None):
    """Closes the connection to warehouse database

        Args:
            conn (ConnectionManager): An instance of connection
    """
    try:
        if conn is None:
            conn = connect()
        br = _browser()
        br.connect(conn)
        br.close()
        del br
        return True
    except Exception:
        return False
