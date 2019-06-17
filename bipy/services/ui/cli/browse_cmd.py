"""Module as an interface to the Warehouse Browser APIs
    available under the namespace `bipy.services.db.warehouse.browser`
    This module should be used by any of the frontend interface,
    like, cli, web, etc

    Author: Ajeet Singh
    Date: 06/17/2019
"""
import hug
from bipy.services.utils import Utility
from bipy.logging import logger

LOGGER = logger.get_logger(__name__)
API = hug.API("browser")


@hug.object(name="browser", version="1.0.0", api=API)
class Browser(object):

    _warehouse_conn = None
    _util = None
    _config = None

    def __init__(self):
        self._util = Utility()
        self._config = self._util.CONFIG

    @hug.object.cli
    def connect(self):
        """Connects to an warehouse database configured through
            configuration file for the system
        """
        try:
            self._warehouse_conn = self._util\
                .get_plugin(self._config.PATH_CONNECTION_MANAGERS)
            self._warehouse_conn.connect(self._config.URL_TEST_DB)
        except Exception:
            raise Exception("Can't connect to warehouse database.\
                          Please check your config file")

    @hug.object.cli
    def schemas(self):
        if self._warehouse_conn is None:
            self.connect()
        browser = self._util.get_plugin(self._config.PATH_BROWSER)
        browser.connect(self._warehouse_conn)
        schemas = browser.get_schemas()
        for schema in schemas:
            print(schema)
        return schemas


@hug.get()
def schemas():
    b = Browser()
    return b.schemas()


if __name__ == "__main__":
    API.cli()
