""" Module to test the Repository Manager class
    Author: Ajeet Singh
    Date: 06/03/2019
"""
from yapsy.PluginManager import PluginManager
from bipy.core.constants import URLS, PATHS
from bipy.core.db.categories import SQLite


class RepositoryManagerTestCase():
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
        print("Warehouse Connection: " + str(self.__conn_wh))
        self.__conn_wh.connect(URLS.TEST_DB)
        #---------- Load Warehouse Browser plugin -----------------------
        self.__plugin_mgr.setPluginPlaces([PATHS.BROWSERS])
        self.__plugin_mgr.locatePlugins()
        browsers = self.__plugin_mgr.loadPlugins()
        self.__browser = browsers[0].plugin_object
        self.__browser.connect(self.__conn_wh)
        print("Browser: " + str(self.__browser))
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
        self.__conn_repo.get_engine().execute("delete from repository_warehouse_databases")
        self.__conn_repo.get_engine().execute("delete from repository_warehouse_schemas")
        self.__conn_repo.get_engine().execute("delete from repository_warehouse_tables")
        self.__conn_repo.get_engine().execute("delete from repository_warehouse_columns")

    def test_save_and_get_db(self):
        """ Test the repository managers functionality for saving and reading \
        back the database meta properties
        """
        try:
            self.__repo_db_meta = self.__meta_gen.generate_database_meta("SQLITE",\
                                                                  URLS.TEST_DB, "User", "Pass")
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

    def test_save_and_get_column(self):
        """ Test the functionality to save and read back the column meta properties \
        of a given table
        """
        try:
            if self.__repo_table_meta is None:
                self.test_save_and_get_table()
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



if __name__ == "__main__":
    t = RepositoryManagerTestCase()
    t.setUp()
    t.test_save_and_get_column()
