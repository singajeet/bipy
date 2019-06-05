""" Logging module to init and config the logger to be used application wide
    Author: Ajeet Singh
    Date: 6/4/2019
"""
import logging
import logging.config
import json
import os
from bipy.core.constants import PATHS


# If applicable, delete the existing log file to generate a fresh log file during each execution
def get_logger(log_name):
    """ Returns the logger configured using the log_config.json file
    """
    with open(PATHS.LOG_CONFIG_PATH, 'rt') as logging_configuration_file:
        config_dict = json.load(logging_configuration_file)
        handlers = config_dict["handlers"]
        file_handler = handlers["file_handler"]
        file_name = file_handler["filename"]
        file_name = os.path.abspath(os.path.join(PATHS.ROOT_PARENT, file_name))
        #replace the filename with the absolute path to root's parent
        file_handler["filename"] = file_name
        logging.config.dictConfig(config_dict)
        return logging.getLogger(log_name)
