"""
    Test cases for ``MetaGenerator``
    Author: Ajeet Singh
    Date: 05/28/2019
"""
import unittest
from yapsy.PluginManager import PluginManager
from bipy.core.db.categories import SQLite
from bipy.core.constants import PATHS, URLS


class MetaGeneratorTestCase(unittest.TestCase):
    """Yest case for MetaGenerator class
    """
    connection = None
    connections = None
    manager = None
    browser = None
    browsers = None
    bmg = None
    mg = None

    def setUp(self):
        self.manager = PluginManager(categories_filter={'SQLITE': SQLite})
        self.manager.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
        self.locatePlugins()
        self.connections = self.manager.loadPlugins()
