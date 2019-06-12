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
            _pm = PluginManager()
            _pm.setPluginPlaces([PATHS.CONFIG_MGR])
            _pm.locatePlugins()
            configs = _pm.loadPlugins()
            Utility.CONFIG = configs[0].plugin_object.CONFIG
        return Utility.__INSTANCE

    def get_plugin(self, path, p_categories_filter=None):
        """ Returns a plugins available at specified path and of category
            provided as argument
        """
        _pm = PluginManager(categories_filter=p_categories_filter)
        _pm.setPluginPlaces([path])
        _pm.locatePlugins()
        plugins = _pm.loadPlugins()
        plugin = plugins[0].plugin_object
        _pm = None
        plugins = None
        return plugin

    def get_all_plugins(self, path, p_categories_filter=None):
        """ Returns all plugin objects as array available at the specified
            path provided as argument
        """
        _pm = PluginManager(categories_filter=p_categories_filter)
        _pm.setPluginPlaces([path])
        _pm.locatePlugins()
        plugins = _pm.loadPlugins()
        return plugins
