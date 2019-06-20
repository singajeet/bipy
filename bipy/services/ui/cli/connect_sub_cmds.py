"""This modules contains sub commands for the main command CONNECT

    Author: Ajeet Singh
    Date: 06/20/2019
"""
from bipy.services.utils import Utility


class ConnectSubCmds:
    """The connection sub commands class"""

    __INSTANCE = None
    _repo_conn = None
    _warehouse_conn = None

    def __new__(cls):
        if ConnectSubCmds.__INSTANCE is None:
            ConnectSubCmds.__INSTANCE = object.__new__(cls)
        return ConnectSubCmds.__INSTANCE

    def connect_warehouse(self, params):
        """Connects to either warehouse or repo based on params passed
        """
        if params.__len__() == 0:
            if self._warehouse_conn is None:
                util = Utility()
                config = util.CONFIG
                self._warehouse_conn = util.get_plugin(config.PATH_CONNECTION_MANAGERS)
                self._warehouse_conn.connect(config.URL_TEST_DB)
            return self._warehouse_conn
        elif str(params[0]).lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("Connects to an Warehouse database configured in the system")
            print("No parameters are required to run this command")
            print("")

    def connect_repo(self, params):
        """Connects to either warehouse or repo based on params passed
        """
        if params.__len__() == 0:
            if self._repo_conn is None:
                util = Utility()
                config = util.CONFIG
                self._repo_conn = util.get_plugin(config.PATH_CONNECTION_MANAGERS)
                self._repo_conn.connect(config.URL_META_DB)
            return self._repo_conn
        elif str(params[0]).lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("Connects to an Repository database configured in the system")
            print("No parameters are required to run this command")
            print("")

    def disconnect(self, params):
        """Disconnects the connection to browser and warehouse

            Args:
                params (Array): An array of string params
        """
        if params.__len__() == 0:
            print("Disconnected successfully!")
            if self._warehouse_conn is not None:
                del self._warehouse_conn
            if self._repo_conn is not None:
                del self._repo_conn
        elif str(params[0]).lower() == "--help":
            print("")
            print("HELP:")
            print("-----")
            print("Closes an Connection to an Warehouse database configured in the system")
            print("No parameters are required to run this command")
            print("")
