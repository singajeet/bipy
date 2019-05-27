""" Shared constants to be use in the application globally
    Author: Ajeet Singh
    Date: 05/27/2019
"""
import os


class PATHS:
    """ Various paths to available modules in the application
    """
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    ROOT_PARENT = os.path.abspath(os.path.join(ROOT, "../"))
    CORE = os.path.abspath(os.path.join(ROOT, "core"))
    DB = os.path.abspath(os.path.join(CORE, "db"))
    WAREHOUSE = os.path.abspath(os.path.join(DB, "warehouse"))
    BROWSERS = os.path.abspath(os.path.join(WAREHOUSE, "browsers"))
    BASE_META_GEN = os.path.abspath(os.path.join(WAREHOUSE, "base_meta_gen"))
    CONNECTION_MANAGERS = os.path.abspath(os.path.join(DB, "connection_managers"))
    REPOSITORY = os.path.abspath(os.path.join(DB, "repository"))
    ANALYTIC = os.path.abspath(os.path.join(DB, "analytic"))


class URLS:
    """ Various URLs used application wise
    """
    TEST_DB = "sqlite:///" + PATHS.ROOT_PARENT + "/test.db"