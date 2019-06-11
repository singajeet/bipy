""" Utility class with various utility methods
    Author: Ajeet Singh
    Date: 06/11/2019
"""
from yapsy.PluginManager import PluginManager
from bipy.services.constants import PATHS


class Utility:
    """ Utility class as singleton
    """

    __INSTANCE = None
    CONFIG = None

    def __new__(cls):
        if Utility.__INSTANCE is None:
            Utility.__INSTANCE = object.__new__(cls)
            pm = PluginManager()
            pm.setPluginPlaces([PATHS.CONFIG_MGR])
            pm.locatePlugins()
            configs = pm.loadPlugins()
            Utility.CONFIG = configs[0].plugin_object.CONFIG
        return Utility.__INSTANCE
