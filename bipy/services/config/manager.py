"""
    Module for system wide configuration management
    Author: Ajeet Singh
    Date: 06/09/2019
"""
from config import Config
import os
from bipy.services.constants import PATHS
# from bipy.logging import logger
from bipy.services import constants
from bipy.services.db import categories

# LOGGER = logger.get_logger(__name__)


class ConfigManager(categories.AbstractCategory):
    """ Singleton class to work with comfiguration
    by whole system
    """

    __INSTANCE = None
    __config_dir = None
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
        # LOGGER.debug("ConfigManaqer instance created")
        self.__config_dir = PATHS.CONFIG_FILES
        self.__config_file = os.path.abspath(
            os.path.join(self.__config_dir, "default.cfg"))
        _cf = open(self.__config_file)
        self.CONFIG = Config(_cf)
        self.CONFIG.addNamespace(constants)
        # LOGGER.debug("Config file opened available at '%s'" %
        #             self.__config_file)

    def set_location(self, new_path):
        """Sets a new path of config file instead of using
        default"""
        self.__config_file = os.path.abspath(new_path)
        self.__config_dir = os.path.abspath(os.path.
                                            dirname(self.__config_file))
        _cf = open(self.__config_file)
        self.CONFIG = Config(_cf)
        self.CONFIG.addNamespace(constants)
        # LOGGER.debug("New location set of config file at: '%s'" %
        #             self.__config_file)

    def get_file_location(self):
        """Returns location of config file"""
        return self.__config_file

    def get_dir_location(self):
        """Returns dir of config file """
        return self.__config_dir

    def get_config(self):
        """ Returns config instance """
        return self.CONFIG
