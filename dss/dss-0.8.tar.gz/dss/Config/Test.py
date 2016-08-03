from Config.Controller.CoreController import *
from Config.Controller.PluginController import *
from Config.View.Core.MasterView import MakeCoreView
from Config.View.Plugin.MasterView import MakePluginsView

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE_NAME = 'config.json'

# CoreController(BASE_DIR, CONFIG_FILE_NAME)
# MakeCoreView(BASE_DIR, CONFIG_FILE_NAME)
PluginsController(BASE_DIR, CONFIG_FILE_NAME)
MakePluginsView(BASE_DIR, CONFIG_FILE_NAME)
