""" Shared constants to be use in the application globally
    Author: Ajeet Singh
    Date: 05/27/2019
"""
import os


class PATHS:
    """ Various paths to available modules in the application
    """
    # ############# DO NOT DELETE BELOW LINE #############################
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    # ############# DO NOT DELETE THE ABOVE LINE #########################
    ROOT_PARENT = os.path.abspath(os.path.join(ROOT, "../"))
    SERVICES = os.path.abspath(os.path.join(ROOT, "services"))
    DATA_FILES = os.path.abspath(os.path.join(ROOT, "data"))
    CONFIG_FILE = os.path.abspath(os.path.join(ROOT, "config/default.cfg"))
    CONFIG_MGR = os.path.abspath(os.path.join(SERVICES, "config"))


class URLS:
    """ Various URLs used application wise
    """
    TEST_DB = "sqlite:///" + PATHS.DATA_FILES + "/test.db"
    META_DB = "sqlite:///" + PATHS.DATA_FILES + "/meta.db"
