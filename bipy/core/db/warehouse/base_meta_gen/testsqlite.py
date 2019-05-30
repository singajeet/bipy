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
    tables = None
    views = None
    columns = None

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
        tbl_list = self.browser.get_tables()
        tbl_list.remove('sqlite_sequence') #remove table used for sequence
        self.tables = self.mg.generate_tables_meta(tbl_list,
                                                  self.schema[0], self.browser)
        assert self.tables.__repr__() == """[Warehouse Table [Name=CUSTOMER_MASTER, SchemaId=-1], Warehouse Table [Name=PRODUCT_MASTER, SchemaId=-1], Warehouse Table [Name=SALES_DETAILS, SchemaId=-1]]"""

    def testMGViewObject(self):
        if self.schema is None:
            self.testMGSchemaObject()
        self.views = self.mg.generate_views_meta(self.browser.get_views(),
                                                 self.schema[0], self.browser)
        assert self.views.__repr__() == '[Warehouse View [Name=revenue_details, SchemaId=-1]]'

    def testMGColumnObject(self):
        if self.tables is None:
            self.testMGTableObject()
        #self.tables[1] is an instance of product_master table
        self.columns = self.mg.generate_columns_meta(self.browser.get_columns('product_master'), self.tables[1], self.browser)
        assert self.columns[0].__repr__() == 'Warehouse Column [Name=id, TypeId=2, TableId=-1, ViewId=-1, MViewId=-1]'


def suite():
    suite = testsqlite.suite()
    suite.addTest(MetaGeneratorTestCase("testMetaGeneratorPluginCount"))
    suite.addTest(MetaGeneratorTestCase("testMetaGeneratorPluginName"))
    suite.addTest(MetaGeneratorTestCase("testMGDatabaseObject"))
    suite.addTest(MetaGeneratorTestCase("testMGSchemaObject"))
    suite.addTest(MetaGeneratorTestCase("testMGTableObject"))
    suite.addTest(MetaGeneratorTestCase("testMGViewObject"))
    suite.addTest(MetaGeneratorTestCase("testMGColumnObject"))
    return suite

if __name__ == "__main__":
    unittest.main()
