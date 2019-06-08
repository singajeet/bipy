"""

 Various decorators for security ppurpose
 Author: Ajeet Singh
 Date: 5/15/2019

"""
from yapsy.PluginManager import PluginManager
from bipy.core.security.manager import SecurityManager
from bipy.core.db import categories
from bipy.core.db.constants import PATHS, URLS


def authorize(privilege):
    def do_authorization(func):
        def wrapper(*args, **kwargs):
            # Authorization logic will go here
            # Get current logged in user
            # if user have role for current privilege
            # execute function
            pm = PluginManager(
                               categories_filter={"SQLITE": categories.SQLite})
            pm.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
            pm.locatePlugins()
            cms = pm.loadPlugins()
            cm = cms[0].plugin_object
            cm.connect(URLS.META_DB)
            sm = SecurityManager(cm)
            curr_user = sm.get_current_user()
            result = sm.authorize(curr_user, privilege)
            if result:
                func(*args, **kwargs)
            # else throw exception
            else:
                raise Exception("User is not authorized \
                                to use this ffunctionality")
        return wrapper
    return do_authorization
