import gtk
from core.core import Core
from GUI.dss_gui import DSS_GUI

core = Core()

if __name__ == "__main__":
    DSS_GUI(core)
    gtk.main()
