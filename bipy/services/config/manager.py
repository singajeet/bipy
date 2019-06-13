"""
    Module for system wide configuration management
    Author: Ajeet Singh
    Date: 06/09/2019
"""
from config import Config
import os
from bipy.services.constants import PATHS
from bipy.services import constants
from bipy.services.db import categories


class ConfigManager(categories.AbstractCategory):
    """ Singleton class to work with comfiguration
    by whole system
    """

    __INSTANCE = None
    __config_file = None
    CONFIG = None

    def __new__(cls):
        """Method overwrite to implement singleton
        class
        """
        if ConfigManager.__INSTANCE is None:
            ConfigManager.__INSTANCE = object.__new__(cls)
        return ConfigManager.__INSTANCE

    def __init__(self):
        """ Default conatructor """
        self.__config_file = os.path.abspath(PATHS.CONFIG_FILE)
        _cf = open(self.__config_file)
        self.CONFIG = Config(_cf)
        self.CONFIG.addNamespace(constants)

    def set_location(self, new_path):
        """Sets a new path of config file instead of using
        default"""
        self.__config_file = os.path.abspath(new_path)
        _cf = open(self.__config_file)
        self.CONFIG = Config(_cf)
        self.CONFIG.addNamespace(constants)

    def get_file_location(self):
        """Returns location of config file"""
        return self.__config_file

    def get_config(self):
        """ Returns config instance """
        return self.CONFIG
