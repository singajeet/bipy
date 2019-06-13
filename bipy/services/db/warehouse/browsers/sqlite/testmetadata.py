"""
    Test cases for ``Browser`` class
    Author: Ajeet Singh
    Date: 05/27/2019
"""
import unittest
from bipy.services.db.categories import SQLite
from bipy.services.utils import Utility


class BrowserTestCase(unittest.TestCase):
    """Test case for Browser class and its methods
    """
    connection = None
    connections = None
    manager = None
    browser = None
    browsers = None
    conf = None

    def setUp(self):
        util = Utility()
        self.conf = util.CONFIG
        self.connections = util.get_all_plugins(
            self.conf.PATH_CONNECTION_MANAGERS,
            {'SQLITE': SQLite})
        self.browsers = util.get_all_plugins(self.conf.PATH_BROWSER,
                                             {'SQLITE': SQLite})

    def testConnectionPluginCount(self):
        assert self.connections.__len__() == 1

    def testBrowserPluginCount(self):
        assert self.browsers.__len__() == 1

    def testConnectionPluginName(self):
        assert self.connections[0].name == 'SQLite Connection Manager'

    def testBrowserPluginName(self):
        assert self.browsers[0].name == 'SQLite Metadata Browser'

    def testConnection(self):
        try:
            self.connection = self.connections[0].plugin_object
            self.connection.connect(self.conf.URL_TEST_DB)
        except Exception:
            self.fail("Exception thrown while connecting to DB")

    def testBrowserConnection(self):
        try:
            self.browser = self.browsers[0].plugin_object
            if self.connection is None:
                self.testConnection()
            self.browser.connect(self.connection)
        except Exception:
            self.fail("Exception thrown while connecting to browser instance")

    def testBrowseSchemas(self):
        if self.browser is None:
            self.testBrowserConnection()
        assert self.browser.get_schemas() == ['main']

    def testBrowseTables(self):
        if self.browser is None:
            self.testBrowserConnection()
        assert self.browser.get_tables() == ['CUSTOMER_MASTER', 'PRODUCT_MASTER', 'SALES_DETAILS', 'android_metadata', 'sqlite_sequence']


def suite():
    suite = unittest.TestSuite()
    suite.addTest(BrowserTestCase("testConnectionPluginCount"))
    suite.addTest(BrowserTestCase("testBrowserPluginCount"))
    suite.addTest(BrowserTestCase("testConnectionPluginName"))
    suite.addTest(BrowserTestCase("testBrowserPluginName"))
    suite.addTest(BrowserTestCase("testConnection"))
    suite.addTest(BrowserTestCase("testBrowserConnection"))
    suite.addTest(BrowserTestCase("testBrowseSchemas"))
    suite.addTest(BrowserTestCase("testBrowseTables"))
    return suite


if __name__ == "__main__":
    unittest.main()
