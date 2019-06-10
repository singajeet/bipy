""" Module to test the Repository Manager class
    Author: Ajeet Singh
    Date: 06/03/2019
"""
import unittest
from yapsy.PluginManager import PluginManager
from bipy.core.constants import URLS, PATHS
from bipy.core.db.categories import SQLite


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

    def setUp(self):
        """ Setups the test case for testing the repo mgr class
        """
        self.__plugin_mgr = PluginManager(categories_filter={"SQLITE": SQLite})
        #---------- Load Connection Mgr plugin for Warehouse ------------
        self.__plugin_mgr.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
        self.__plugin_mgr.locatePlugins()
        conns = self.__plugin_mgr.loadPlugins()
        self.__conn_wh = conns[0].plugin_object
        self.__conn_wh.connect(URLS.TEST_DB)
        #---------- Load Warehouse Browser plugin -----------------------
        self.__plugin_mgr.setPluginPlaces([PATHS.BROWSERS])
        self.__plugin_mgr.locatePlugins()
        browsers = self.__plugin_mgr.loadPlugins()
        self.__browser = browsers[0].plugin_object
        self.__browser.connect(self.__conn_wh)
        #--------- Load Base Meta Generator plugin ----------------------
        self.__plugin_mgr.setPluginPlaces([PATHS.BASE_META_GEN])
        self.__plugin_mgr.locatePlugins()
        base_meta_gen = self.__plugin_mgr.loadPlugins()
        self.__meta_gen = base_meta_gen[0].plugin_object
        #--------- Load Repository Manager plugin -----------------------
        self.__plugin_mgr.setPluginPlaces([PATHS.REPO_MGR])
        self.__plugin_mgr.locatePlugins()
        repo_mgrs = self.__plugin_mgr.loadPlugins()
        self.__repo_mgr = repo_mgrs[0].plugin_object
        #----- Load Connection Mgr plugin for repository / meta db ------
        self.__plugin_mgr = PluginManager(categories_filter={"SQLITE": SQLite})
        self.__plugin_mgr.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
        self.__plugin_mgr.locatePlugins()
        repo_conns = self.__plugin_mgr.loadPlugins()
        self.__conn_repo = repo_conns[0].plugin_object
        self.__conn_repo.connect(URLS.META_DB)
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
