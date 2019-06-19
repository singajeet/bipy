"""This module integrates the base_meta_gen with repository modules to save and read
    the required DB objects from Warehouse Database.

    Author: Ajeet Singh
    Date: 0/19/2019
"""
import hug
from bipy.services.utils import Utility


def _connect():
    """Connects to an repository database for storing and reading back the metadata objects
    """
    utils = Utility()
    config = utils.CONFIG
    conn = utils.get_plugin(config.PATH_CONNECTION_MANAGERS)
    conn.connect(config.URL_META_DB)
    return conn


def _base_meta_gen():
    """Returns an instance of base meta generator"""
    util = Utility()
    config = util.CONFIG
    bmg = util.get_plugin(config.PATH_BASE_META_GEN)
    return bmg


def _repo_manager(conn):
    """Returns an instance of repository manager"""
    util = Utility()
    config = util.CONFIG
    repo_mgr = util.get_plugin(config.PATH_REPO_MGR)
    repo_mgr.connect(conn)
    return repo_mgr


@hug.cli()
@hug.get()
def create_database(db_name, db_type, db_url, user, password, conn=None):
    """Create database Meta objects and save back to repoistory

        Args:
            db_name (String): A label of database to refer
            db_type (String): Type of database i.e., SQLITE, MYSQL, etc
            db_url (String): A connection url to the database
            user (String): A username to connect to database
            password (String): password for the username passed
    """
    try:
        if conn is None:
            conn = _connect()
        bmg = _base_meta_gen()
        rm = _repo_manager(conn)
        db_obj = bmg.generate_database_meta(db_name, db_type, db_url,
                                            user, password)
        rm.save(db_obj)
        return ("Database Meta Object: '%s' has been created successfully!" % (db_obj))
    except Exception as err:
        return "Database Meta Object creation failed => %s" % (err)
