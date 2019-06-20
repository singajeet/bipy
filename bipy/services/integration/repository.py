"""This module integrates the base_meta_gen with repository modules to save and read
    the required DB objects from Warehouse Database.

    Author: Ajeet Singh
    Date: 0/19/2019
"""
import hug
from bipy.services.utils import Utility


def _repo_connect():
    """Connects to an repository database for storing and reading back the metadata objects
    """
    utils = Utility()
    config = utils.CONFIG
    conn = utils.get_plugin(config.PATH_CONNECTION_MANAGERS)
    conn.connect(config.URL_META_DB)
    return conn


def _wh_connect():
    """Connects to an repository database for storing and reading back the metadata objects
    """
    utils = Utility()
    config = utils.CONFIG
    conn = utils.get_plugin(config.PATH_CONNECTION_MANAGERS)
    conn.connect(config.URL_TEST_DB)
    return conn


def _browser(wh_conn):
    """Returns instance of database browser"""
    util = Utility()
    config = util.CONFIG
    br = util.get_plugin(config.PATH_BROWSER)
    br.connect(wh_conn)
    return br


def _base_meta_gen():
    """Returns an instance of base meta generator"""
    util = Utility()
    config = util.CONFIG
    bmg = util.get_plugin(config.PATH_BASE_META_GEN)
    return bmg


def _repo_manager(repo_conn):
    """Returns an instance of repository manager"""
    util = Utility()
    config = util.CONFIG
    repo_mgr = util.get_plugin(config.PATH_REPO_MGR)
    repo_mgr.connect(repo_conn)
    return repo_mgr


@hug.cli()
@hug.get()
def create_database(db_name, db_type, db_url, user, password, repo_conn=None):
    """Create database Meta objects and save back to repoistory

        Args:
            db_name (String): A label of database to refer
            db_type (String): Type of database i.e., SQLITE, MYSQL, etc
            db_url (String): A connection url to the database
            user (String): A username to connect to database
            password (String): password for the username passed
    """
    try:
        if repo_conn is None:
            repo_conn = _repo_connect()
        bmg = _base_meta_gen()
        rm = _repo_manager(repo_conn)
        db_obj = bmg.generate_database_meta(db_name, db_type, db_url,
                                            user, password)
        rm.save(db_obj)
        return ("Database Meta Object: '%s' has been created successfully!" % (db_obj))
    except Exception as err:
        return "Database Meta Object creation failed => %s" % (err)


@hug.cli()
@hug.get()
def create_schemas(schema_list, database, repo_conn=None):
    """Creates schema objects and save it to the repoaitory

        Args:
            schema_list (String): A list of schema names seperated by ',' character
                                    without any space inbetween. eg,
                                    schema1,schema2,schema3
            database (String): Name of database underwhich these schemas needs to
                                be created
    """
    try:
        if repo_conn is None:
            repo_conn = _repo_connect()
        bmg = _base_meta_gen()
        rm = _repo_manager(repo_conn)
        db = rm.get_database(database)
        if db is not None:
            schema_arr = str(schema_list).split(',')
            schemas = bmg.generate_schemas_meta(schema_arr, db)
            rm.save_all(schemas)
            return "Schema objects '%s' created successfully!" % (schemas)
        else:
            return "Schema meta objects creation failed=> No such database found: %s" % (database)
    except Exception as err:
        return "Schema meta objects creation failed=> %s" % (err)


@hug.cli()
@hug.get()
def create_tables(table_list, schema, repo_conn=None, wh_conn=None):
    """Create tables objects and save it in the repository

        Args:
            table_list (String): List of table names seperated with ',' character
                                    with no space in between, eg.,
                                    table1,table2,table3
            schema (String): Name of schema under which tables needs to be created
            repo_conn (ConnectionManager): A connection to repository database
            wh_conn (ConnectionManager): A connecrion to warehouse database
    """
    try:
        if repo_conn is None:
            repo_conn = _repo_connect()
        if wh_conn is None:
            wh_conn = _wh_connect()
        bmg = _base_meta_gen()
        br = _browser(wh_conn)
        rm = _repo_manager(repo_conn)
        sch = rm.get_schema(schema)
        if sch is not None:
            table_arr = str(table_list).split(',')
            tables = bmg.generate_tables_meta(table_arr, sch, br)
            rm.save_all(tables)
            return "Tables objects created successfully: %s" % (tables)
        else:
            return "Tables meta objects creation failed=> No such schema found: %s" % (schema)
    except Exception as err:
        return "Tables meta objects creation failed=> %s" % (err)
