"""

 Various decorators for security purpose
 Author: Ajeet Singh
 Date: 5/15/2019

"""
from bipy.services.security.manager import SecurityManager
from bipy.services.utils import Utility


def authorize(privilege):
    """Decorator to check authorization of a user for given method in class
        User will be able to execute method if the privilege is available to
        user from various roles assigned to it
    """
    def do_authorization(func):
        """Returns the authorization wrapper object which will further execute
            authorization logic before calling the decorated methd
        """
        def wrapper(*args, **kwargs):
            """ Authorization logic that will init the SecurityManager class
                and executes the logic to check whether function call
                is allowed or not
            """
            util = Utility()
            conf = util.CONFIG
            cms = util.get_all_plugins(conf.PATH_CONNECTION_MANAGERS)
            _cm = cms[0].plugin_object
            _cm.connect(conf.URL_META_DB)
            _sm = SecurityManager(_cm)
            result = _sm.authorize(privilege)
            if result:
                func(*args, **kwargs)
            # else throw exception
            else:
                raise Exception("User is not authorized \
                                to use this functionality")
        return wrapper
    return do_authorization
