"""
    Test cases for ``MetaGenerator``
    Author: Ajeet Singh
    Date: 05/28/2019
"""
import unittest
from bipy.core.constants import PATHS, URLS
from bipy.core.db.warehouse.browsers import testsqlite


class MetaGeneratorTestCase(testsqlite.BrowserTestCase):
    """Yest case for MetaGenerator class
    """
    bmg = None
    mg = None
    db = None
    schema = None
    table = None

    def setUp(self):
        testsqlite.BrowserTestCase.setUp(self)
        self.manager.setPluginPlaces([PATHS.BASE_META_GEN])
        self.manager.locatePlugins()
        self.bmg = self.manager.loadPlugins()

    def testMetaGeneratorPluginCount(self):
        assert self.bmg.__len__() == 1

    def testMetaGeneratorPluginName(self):
        assert self.bmg[0].name == 'SQLite MetaData Generator'

    def testMGDatabaseObject(self):
        self.mg = self.bmg[0].plugin_object
        self.db = self.mg.generate_database_meta("SQLITE", URLS.TEST_DB, "user", "pass")
        assert self.db.__repr__() == 'Warehouse [Name=None, Type=SQLITE]'

    def testMGSchemaObject(self):
        if self.mg is None:
            self.testMGDatabaseObject()
        if self.browser is None:
            self.testBrowserConnection()
        self.schema = self.mg.generate_schemas_meta(self.browser.get_schemas(), self.db)
        assert self.schema.__repr__() == '[Warehouse Schema [Name=main]]'

    def testMGTableObject(self):
        if self.schema is None:
            self.testMGSchemaObject()
        self.table = self.mg.generate_tables_meta(self.browser.get_tables(),
                                                  self.schema, self.browser)
        assert self.table.__repr__() == '[]'


def suite():
    suite = testsqlite.suite()
    suite.addTest(MetaGeneratorTestCase("testMetaGeneratorPluginCount"))
    suite.addTest(MetaGeneratorTestCase("testMetaGeneratorPluginName"))
    suite.addTest(MetaGeneratorTestCase("testMGDatabaseObject"))
    suite.addTest(MetaGeneratorTestCase("testMGSchemaObject"))
    suite.addTest(MetaGeneratorTestCase("testMGTableObject"))
    return suite

if __name__ == "__main__":
    unittest.main()
