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
