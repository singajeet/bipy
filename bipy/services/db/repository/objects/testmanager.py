""" Module to test the Repository Manager class
    Author: Ajeet Singh
    Date: 06/03/2019
"""
import unittest
from bipy.services.db.categories import SQLite
from bipy.services.utils import Utility

class RepositoryManagerTestCase(unittest.TestCase):
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
    __conf = None

    def setUp(self):
        """ Setups the test case for testing the repo mgr class
        """
        utils = Utility()
        self.__conf = utils.CONFIG
        #---------- Load Connection Mgr plugin for Warehouse ------------
        conns = utils.get_all_plugins(self.__conf.PATH_CONNECTION_MANAGERS)
        self.__conn_wh = conns[0].plugin_object
        self.__conn_wh.connect(self.__conf.URL_TEST_DB)
        #---------- Load Warehouse Browser plugin -----------------------
        browsers = utils.get_all_plugins(self.__conf.PATH_BROWSER)
        self.__browser = browsers[0].plugin_object
        self.__browser.connect(self.__conn_wh)
        #--------- Load Base Meta Generator plugin ----------------------
        base_meta_gen = utils.get_all_plugins(self.__conf.PATH_BASE_META_GEN)
        self.__meta_gen = base_meta_gen[0].plugin_object
        #--------- Load Repository Manager plugin -----------------------
        repo_mgrs = utils.get_all_plugins(self.__conf.PATH_REPO_MGR)
        self.__repo_mgr = repo_mgrs[0].plugin_object
        #----- Load Connection Mgr plugin for repository / meta db ------
        repo_conns = utils.get_all_plugins(self.__conf.PATH_CONNECTION_MANAGERS)
        self.__conn_repo = repo_conns[0].plugin_object
        self.__conn_repo.connect(self.__conf.URL_META_DB)
        self.__repo_mgr.connect(self.__conn_repo)

    def test_save_and_get_db(self):
        """ Test the repository managers functionality for saving and reading \
        back the database meta properties
        """
        try:
            self.__conn_repo\
                .get_engine().execute("delete from\
                                      repository_warehouse_databases")
            self.__repo_db_meta = self.__meta_gen\
                .generate_database_meta("Warehouse 1","SQLITE",
                                        self.__conf.URL_TEST_DB,
                                        "User", "Pass")
            self.__repo_db_meta.name = "Warehouse 1"
            self.__repo_mgr.save(self.__repo_db_meta)
        except Exception:
            self.fail("Unable to create database meta")
        db_names = self.__repo_mgr.get_database_names()
        assert db_names.__len__() == 1
        assert db_names[0] == "Warehouse 1"

    def test_save_and_get_schema(self):
        """ Test the repository managers functionality to save and read the schema \
        metadata properties
        """
        try:
            if self.__repo_db_meta is None:
                self.test_save_and_get_db()
            self.__conn_repo.get_engine().execute("delete from repository_warehouse_schemas")
            schema_list = self.__browser.get_schemas()
            self.__repo_schema_meta = self.__meta_gen\
                    .generate_schemas_meta(schema_list, self.__repo_db_meta)
            self.__repo_mgr.save_all(self.__repo_schema_meta)
        except Exception:
            self.fail("Unable to create schema meta information")
        schema_names = self.__repo_mgr.get_all_schema_names()
        assert schema_names.__len__() == 1
        assert schema_names[0] == "main"

    def test_save_and_get_table(self):
        """ Test's the repository manager functionality to save and read the tables \
        metadata properties
        """
        try:
            if self.__repo_schema_meta is None:
                self.test_save_and_get_schema()
            self.__conn_repo.get_engine().execute("delete from repository_warehouse_tables")
            table_list = self.__browser.get_tables()
            #---- Will test with only first 3 tables
            table_list = [table_list[0], table_list[1], table_list[2]]
            self.__repo_table_meta = self.__meta_gen\
                    .generate_tables_meta(table_list, self.__repo_schema_meta[0], self.__browser)
            self.__repo_mgr.save_all(self.__repo_table_meta)
        except Exception:
            self.fail("Unable to create table meta information")
        assert self.__repo_table_meta.__len__() == 3
        table_names = self.__repo_mgr.get_all_table_names()
        assert table_names.__len__() == 3
        assert table_names == ['CUSTOMER_MASTER', 'PRODUCT_MASTER', 'SALES_DETAILS']

    def test_save_and_get_view(self):
        """ Test's the repoaitory manager functionality to save and read the views \
        metadata properties
        """
        try:
            if self.__repo_schema_meta is None:
                self.test_save_and_get_schema()
            self.__conn_repo.get_engine().execute("delete from repository_warehouse_views")
            view_list = self.__browser.get_views()
            self.__repo_view_meta = self.__meta_gen\
                .generate_views_meta(view_list, self.__repo_schema_meta[0], self.__browser)
            self.__repo_mgr.save_all(self.__repo_view_meta)
        except Exception:
            self.fail("Unable to create view meta information")
        assert self.__repo_view_meta.__len__() == 1

    def test_save_and_get_column(self):
        """ Test the functionality to save and read back the column meta properties \
        of a given table
        """
        try:
            if self.__repo_table_meta is None:
                self.test_save_and_get_table()
            self.__conn_repo.get_engine().execute("delete from repository_warehouse_columns")
            for table in self.__repo_table_meta:
                column_list = self.__browser.get_columns(table.name)
                self.__repo_column_meta = self.__meta_gen\
                        .generate_columns_meta(column_list, table, self.__browser)
                self.__repo_mgr.save_all(self.__repo_column_meta)
        except Exception:
            self.fail("Unable to create column meta information")
        assert self.__repo_table_meta.__len__() == 3
        for table in self.__repo_table_meta:
            column_names = self.__repo_mgr.get_all_column_names(table)
            if table.name == "SALES_DETAILS":
                assert column_names.__len__() == 4
            else:
                assert column_names.__len__() == 3


def load_tests(loader, tests, pattern):
    """Function to create test suite for execution of test methods
    """
    suite = unittest.TestSuite()
    suite.addTest(RepositoryManagerTestCase("test_save_and_get_db"))
    suite.addTest(RepositoryManagerTestCase("test_save_and_get_schema"))
    suite.addTest(RepositoryManagerTestCase("test_save_and_get_table"))
    suite.addTest(RepositoryManagerTestCase("test_save_and_get_column"))
    suite.addTest(RepositoryManagerTestCase("test_save_and_get_view"))
    return suite

if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_loader.sortTestMethodsUsing = None
    unittest.main(testLoader=test_loader)
