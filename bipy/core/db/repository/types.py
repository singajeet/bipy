"""Enums for all different types of data supported by the system
  Author: Ajeet Singh
  Date: 5/18/2019
"""
from enum import Enum, unique


class AutoNumber(Enum):
    """
        Class to generate numbers automatically and assign the unique value to each ENUM defined
    """

    def __new__(cls):
        """
            Constructor of the Autonumber class

            Args:
                cls (object): Argument passed to this class
        """
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

@unique
class DataTypes(AutoNumber):
    """Enum for all different data types
    """
    NUMERIC = ()
    INTEGER = ()
    DECIMAL = ()
    FLOAT = ()
    LONG = ()
    CHAR = ()
    STRING = ()
    VARCHAR = ()
    VARCHAR2 = ()
    DATE = ()
    TIME = ()
    DATETIME = ()
    ZONE = ()
    LOCALZONE = ()
    TIMEZONE = ()
    BOOLEAN = ()

@unique
class ViewTypes(AutoNumber):
    """Enum for different type of views
    """
    VIEW = ()
    MATERIALIZED_VIEW = ()
