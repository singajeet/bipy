""" Module to test the Repository Manager class
    Author: Ajeet Singh
    Date: 06/03/2019
"""
import unittest
from yapsy.PluginManager import PluginManager
from bipy.services.constants import URLS, PATHS
from bipy.services.db.categories import SQLite
from bipy.services.utils import Utility


class RepositoryRelationshipManagerTestCase(unittest.TestCase):
    """Testcase for Repository Maager
    """
    __plugin_mgr = None
    __conn_wh = None
    __browser = None
    __meta_gen = None
    __repo_mgr = None
    __conn_repo = None
    __repo_db_meta = None
    __repo_schema_meta = None
    __repo_table_meta = None
    __repo_column_meta = None
    conf = None

    def setUp(self):
        """ Setups the test case for testing the repo mgr class
        """
        util = Utility()
        self.conf = util.CONFIG
        #---------- Load Connection Mgr plugin for Warehouse ------------
        conns = util.get_all_plugins(self.conf.PATH_CONNECTED_SESSION)
        self.__conn_wh = conns[0].plugin_object
        self.__conn_wh.connect(self.conf.URL_TEST_DB)
        #---------- Load Warehouse Browser plugin -----------------------
        browsers = util.get_all_plugins(self.conf.PATH_BROWSER)
        self.__browser = browsers[0].plugin_object
        self.__browser.connect(self.__conn_wh)
        #--------- Load Base Meta Generator plugin ----------------------
        base_meta_gen = util.get_all_plugins(self.conf.PATH_BASE_META_GEN)
        self.__meta_gen = base_meta_gen[0].plugin_object
        #--------- Load Repository Manager plugin -----------------------
        repo_mgrs = util.get_all_plugins(self.conf.PATH_REPO_MGR)
        self.__repo_mgr = repo_mgrs[0].plugin_object
        #----- Load Connection Mgr plugin for repository / meta db ------
        repo_conns = util.get_all_plugins(self.conf.PATH_CONNECTION_MANAGERS)
        self.__conn_repo = repo_conns[0].plugin_object
        self.__conn_repo.connect(self.conf.URL_META_DB)
        self.__repo_mgr.connect(self.__conn_repo)


def load_tests(loader, tests, pattern):
    """Function to create test suite for execution of test methods
    """
    suite = unittest.TestSuite()
    #suite.addTest(RepositoryRelationshipManagerTestCase("test_save_and_get_view"))
    return suite

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None
    unittest.main(testLoader=test_loader)
