""" Logging module to init and config the logger to be used application wide
    Author: Ajeet Singh
    Date: 6/4/2019
"""
import logging
import logging.config
import json
import os
from bipy.services.utils import Utility


# If applicable, delete the existing log file to generate a fresh log file during each execution
def get_logger(log_name):
    """ Returns the logger configured using the log_config.json file
    """
    util = Utility()
    conf = util.CONFIG
    with open(conf.PATH_LOG_CONFIG, 'rt') as logging_configuration_file:
        config_dict = json.load(logging_configuration_file)
        handlers = config_dict["handlers"]
        file_handler = handlers["file_handler"]
        file_name = file_handler["filename"]
        file_name = os.path.abspath(os.path.join(conf.PATH_ROOT_PARENT, file_name))
        #replace the filename with the absolute path to root's parent
        file_handler["filename"] = file_name
        logging.config.dictConfig(config_dict)
        # Do not show debug and info message from 3rd party
        logging.getLogger("yapsy").setLevel(logging.WARNING)
        return logging.getLogger(log_name)
