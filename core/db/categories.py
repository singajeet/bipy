"""This module lists all the database types as classes that are supported
    by the system. Each class will be used to identify the plugins to be
    loaded based on the db type configured.

    Author: Ajeet Singh
    Date: 5/22/2019
"""
from yapsy.IPlugin import IPlugin



class AbstractCategory(IPlugin):
    """ An abstract category
    """
    name = "AbstractCategory"

    def db_type(self):
        """Returns database type
        """
        return self.name

    def used_by(self):
        """Returns the usage of this plugin i.e., used by Connection
            Manager, Security Manager, etc
        """
        pass

    def __repr__(self):
        """An string representation
        """
        return self.name


class SQLite(IPlugin):
    """ An SQLite db type as category
    """
    name = "SQLITE"


class MariaDB(AbstractCategory):
    """ An MariaDB type as category
    """
    name = "MARIADB"


class MySQL(AbstractCategory):
    """ An MySQL db type category
    """
    name = "MYSQL"


class Oracle(AbstractCategory):
    """ An Oracle DB type as category
    """
    name = "ORACLE"
