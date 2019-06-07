from bipy.core.constants import URLS, PATHS
from bipy.core.db.categories import SQLite
from yapsy.PluginManager import PluginManager
#----------- Create Plugin Mgr instance -------------------------
plugin_mgr = PluginManager(categories_filter={"SQLITE": SQLite})
#---------- Load Connection Mgr plugin for Warehouse ------------
plugin_mgr.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
plugin_mgr.locatePlugins()
conns = plugin_mgr.loadPlugins()
conn_wh = conns[0].plugin_object
conn_wh
conn_wh.connect(URLS.TEST_DB)
#---------- Load Warehouse Browser plugin -----------------------
plugin_mgr.setPluginPlaces([PATHS.BROWSERS])
plugin_mgr.locatePlugins()
browsers = plugin_mgr.loadPlugins()
browser = browsers[0].plugin_object
browser
browser.connect(conn_wh)
#--------- Load Base Meta Generator plugin ----------------------
plugin_mgr.setPluginPlaces([PATHS.BASE_META_GEN])
plugin_mgr.locatePlugins()
base_meta_gen = plugin_mgr.loadPlugins()
meta_gen = base_meta_gen[0].plugin_object
meta_gen
#--------- Load Repository Manager plugin -----------------------
plugin_mgr.setPluginPlaces([PATHS.REPO_MGR])
plugin_mgr.locatePlugins()
repo_mgrs = plugin_mgr.loadPlugins()
repo_mgr = repo_mgrs[0].plugin_object
repo_mgr
#----- Load Connection Mgr plugin for repository / meta db ------
plugin_mgr = PluginManager(categories_filter={"SQLITE": SQLite})
plugin_mgr.setPluginPlaces([PATHS.CONNECTION_MANAGERS])
plugin_mgr.locatePlugins()
repo_conns = plugin_mgr.loadPlugins()
conn_repo = repo_conns[0].plugin_object
conn_repo.connect(URLS.META_DB)
conn_repo
repo_mgr.connect(conn_repo)
#------ Load Repository Relationship Manager ---------------
plugin_mgr.setPluginPlaces([PATHS.REPO_REL_MGR])
plugin_mgr.locatePlugins()
rel_mgrs = plugin_mgr.loadPlugins()
rel_mgr = rel_mgrs[0].plugin_object
rel_mgr.connect(conn_repo, repo_mgr)
