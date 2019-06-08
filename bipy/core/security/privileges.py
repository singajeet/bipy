"""
    Enum definitions for all privileges
    Author: Ajeet Singh
    Date: 5/15/2019
"""
from enum import Enum, unique


class AutoNumber(Enum):
    """
        Class to generate numbers automatically and
        assign the unique value to each ENUM defined
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
class Privileges(AutoNumber):
    """
        An ENUM class defining all the privilege used by the system
    """
    CREATE_METAMODEL_OBJECT = ()
    BROWSE_METAMODEL = ()
    QUERY_METAMODEL_TABLES = ()
    QUERY_METAMODEL_VIEWS = ()
    QUERY_METAMODEL_PROCEDURES = ()
    QUERY_METAMODEL_FUNCTIONS = ()
    QUERY_METAMODEL_SCHEMA = ()
    CONNECT_METADATA = ()
    CONNECT_DB = ()
