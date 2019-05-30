from bipy.core.constants import URLS, PATHS
from bipy.core.db.categories import SQLite
from yapsy.PluginManager import PluginManager
manager = PluginManager(categories_filter={"SQLITE": SQLite})
manager.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
manager.locatePlugins()
conns = manager.loadPlugins()
conn = conns[0].plugin_object
conn
manager.setPluginPlaces([PATHS.BROWSERS])
manager.locatePlugins()
browsers = manager.loadPlugins()
browser = browsers[0].plugin_object
browser
manager.setPluginPlaces([PATHS.BASE_META_GEN])
manager.locatePlugins()
bmg = manager.loadPlugins()
mg = bmg[0].plugin_object
mg
conn.connect(URLS.TEST_DB)
browser.connect(conn)
