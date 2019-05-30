"""
    Module to setup or install the BIPY application
    Author: Ajeet Singh
    Date: 05/31/2019
"""

def install(connection, base):
    """Setups the metadata of all class defined under `base` using the
        engine of the already established `connection` to database
    """
    if connection is None:
        raise Exception("""The `connection` parameter can't be None and should
                        have an active connection to the database""")
    if base is None:
        raise Exception("""The `base` parameter can't be None as all the classes
                        inherting from it will have its metadata defined in DB
                        """)
    base.metadata.bind = connection.get_engine()
    base.metadata.create_all()
