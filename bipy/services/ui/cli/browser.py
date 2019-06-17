"""Browser commands to be used by various interfaces
    like CLI, Web, etc

    Author: Ajeet Singh
    Date: 06/17/2019
"""
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


def schemas(conn):
    """Returns instance of schemas in warehouse

        Args:
            conn (ConnectionManager): connection to warehouse db
    """
    br = _browser()
    br.connect(conn)
    return br.get_schemas()


def tables(conn, schema=None):
    """Returns instance of tables in warehouse

        Args:
            conn (ConnectionManager): connection to warehouse db
            schema (String): Schema name from where tables needs to be listed
    """
    br = _browser()
    br.connect(conn)
    return br.get_tables(schema)


def views(conn, schema=None):
    """Returns instance of views in warehouse

        Args:
            conn (ConnectionManager): connection to warehouse db
            schema (String): Schema name from where views needs to be listed
    """
    br = _browser()
    br.connect(conn)
    return br.get_views(schema)
