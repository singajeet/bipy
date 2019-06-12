"""
    Test Cases for ``ConnectionManager`` class
    Author: Ajeet Singh
    Date: 05/27/2019
"""
import unittest
from yapsy.PluginManager import PluginManager
from bipy.services.db.categories import SQLite
from bipy.services.utils import Utility

class ConnectionManagerTestCase(unittest.TestCase):
    """TestCase for ConnectionManager class and its methods
    """
    connections = None
    conf = None

    def setUp(self):
        util = Utility()
        self.conf = util.CONFIG
        self.connections = util.get_all_plugins(self.conf.PATH_CONNECTION_MANAGERS, {'SQLITE': SQLite})

    def testPluginCount(self):
        assert self.connections.__len__() == 1

    def testPluginName(self):
        assert self.connections[0].name == 'SQLite Connection Manager'

    def testConnect(self):
        try:
            self.connections[0].plugin_object.connect(self.conf.URL_TEST_DB)
        except Exception:
            self.fail("Exception thrown while connecting to DB")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ConnectionManagerTestCase("testPluginCount"))
    suite.addTest(ConnectionManagerTestCase("testPluginName"))
    suite.addTest(ConnectionManagerTestCase("testConnect"))
    return suite


if __name__ == "__main__":
    unittest.main()
