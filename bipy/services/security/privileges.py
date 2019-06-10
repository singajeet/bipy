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
    METAMODEL_CREATE = ()
    METAMODEL_READ = ()
    METAMODEL_REMOVE = ()
    METAMODEL_UPDATE = ()
    METAMODEL_WRITE = ()
    METAMODEL_EXECUTE = ()
    QUERY_METAMODEL_TABLES_READ = ()
    QUERY_METAMODEL_VIEWS_READ = ()
    QUERY_METAMODEL_PROCEDURES_READ = ()
    QUERY_METAMODEL_FUNCTIONS_READ = ()
    QUERY_METAMODEL_SCHEMA_READ = ()
    QUERY_METAMODEL_TABLES_WRITE = ()
    QUERY_METAMODEL_VIEWS_WRITE = ()
    QUERY_METAMODEL_PROCEDURES_WRITE = ()
    QUERY_METAMODEL_FUNCTIONS_WRITE = ()
    QUERY_METAMODEL_SCHEMA_WRITE = ()
    CONNECT_CREATE = ()
    CONNECT_REMOVE = ()
    CONNECT_UPDATE = ()
    CONNECT_READ = ()
    CONNECT_WRITE = ()
    CONNECT_EXECUTE = ()
