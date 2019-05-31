"""
 Class to manager sqlite connections used by various OLAP services
 Author: Ajeet Singh
 Date: 5/12/2019
"""
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import bipy.core.db.categories as categories


class ConnectionManager(categories.SQLite):
    """ A SQLite connection manager which is a singleton and should return same
        instance always

        >>> from bipy.core.db.categories import SQLite

        >>> from yapsy.PluginManager import PluginManager

        >>> from bipy.core.constants import PATHS

        >>> manager = PluginManager(categories_filter={'SQLITE': SQLite})

        >>> manager.setPluginPlaces([PATHS.CONNECTION_MANAGERS])

        >>> manager.locatePlugins()

        >>> connections = manager.loadPlugins()

        >>> connections.__len__()
        1
        >>> connections[0].name
        'SQLite Connection Manager'
        >>>

    """

    connection_string = ""
    ConnectedSession = None
    engine = None
    inspector = None
    Session = None
    __instance = None

    """def __new__(cls):

         The singleton constructor for this

            Args:
                cls (object): cls

            Return:
                ConnectionManager: An singleton instance of this

        if ConnectionManager.__instance is None:
            ConnectionManager.__instance = object.__new__(cls)
        return ConnectionManager.__instance
    """


    def __init__(self):
        """
            Default constructor of the Connection Manager class
        """
        categories.SQLite.__init__(self)


    def connect(self, conn_string):
        """Setups the connection using the connection string passed as param

            Args:
                conn_string (string): The connection string to connect with the
                                        database
        """
        self.connection_string = conn_string
        self.engine = create_engine(conn_string)
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.ConnectedSession = self.Session()
        self.inspector = inspect(self.engine)

    def get_connection_string(self):
        """Returns the connection string used in this for mmaking
            connections to the database
        """
        return self.connection_string

    def get_engine(self):
        """Returns the database engine for SQLite database
        """
        return self.engine

    def get_session(self):
        """Returns an connected session to the database
        """
        return self.ConnectedSession

    def get_inspector(self):
        """Returns an instance of inspector that can be utilized to
            browse through the metadata of the SQLite database
        """
        return self.inspector

    def disconnect(self):
        """Closes the connection made with the SQLite database
        """
        self.ConnectedSession.close_all()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
