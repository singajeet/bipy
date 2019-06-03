"""
    Test Cases for ``ConnectionManager`` class
    Author: Ajeet Singh
    Date: 05/27/2019
"""
import unittest
from yapsy.PluginManager import PluginManager
from bipy.core.db.categories import SQLite
from bipy.core.constants import URLS, PATHS

class ConnectionManagerTestCase(unittest.TestCase):
    """TestCase for ConnectionManager class and its methods
    """
    connection = None
    manager = None

    def setUp(self):
        #self.manager = ConnectionManager()
        self.manager = PluginManager(categories_filter={'SQLITE': SQLite})
        self.manager.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
        self.manager.locatePlugins()
        self.connection = self.manager.loadPlugins()

    def testPluginCount(self):
        assert self.connection.__len__() == 1

    def testPluginName(self):
        assert self.connection[0].name == 'SQLite Connection Manager'

    def testConnect(self):
        try:
            self.connection[0].plugin_object.connect(URLS.TEST_DB)
        except Exception:
            self.fail("Exception thrown while connecting to DB")

    #def testConnectionString(self):
     #   assert self.manager.connection_string == URLS.TEST_DB

    def tearDown(self):
        pass
        #self.connection[0].plugin_object.disconnect()
        #self.connection = None
        #self.manager = None


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ConnectionManagerTestCase("testPluginCount"))
    suite.addTest(ConnectionManagerTestCase("testPluginName"))
    suite.addTest(ConnectionManagerTestCase("testConnect"))
    #suite.addTest(ConnectionManagerTestCase("testConnectionString"))
    return suite


if __name__ == "__main__":
    unittest.main()
    #c = ConnectionManagerTestCase()
    #c.setUp()
    #c.testConnectionString()
