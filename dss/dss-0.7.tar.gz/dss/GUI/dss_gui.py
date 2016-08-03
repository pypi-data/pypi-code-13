import gtk
import schedule
import signal
import subprocess
import status_icon
import json
import os
import shutil, errno
from Config import Runner

PYKEYLOGGER = "pykeylogger"

class DSS_GUI(gtk.Window):
    def __init__(self, core):
        super(DSS_GUI, self).__init__()
        # Call function to me System Tray Icon
        self.test = status_icon.CustomSystemTrayIcon(core, self.show_gui)
        # Set Title and Size of Main Window Frame
        self.set_title("Decision Support System Logger V 1.0")
        self.set_size_request(750, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        self.core = core

        Runner.scaffold_initial_files()

        # Creating Tool Bar
        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_ICONS)

        open_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"), "open.png")))
        open_button.connect("clicked", self.callback)
        #pause_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"pause.png")))
        #pause_button.connect("clicked", self.pause_plugin)
        self.start_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"start.png")))
        self.start_button.connect("clicked", self.start_plugin)
        self.stop_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"stop.png")))
        self.stop_button.connect("clicked", self.stop_plugin)
        self.stop_button.set_sensitive(False)
        seperator = gtk.SeparatorToolItem()
        json_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"json.png")))
        json_button.connect("clicked", self.parse_all, core)
        hide_button = gtk.ToolButton(gtk.image_new_from_file(os.path.join(os.path.join(os.getcwd(), "GUI"),"hide.png")))
        hide_button.connect("clicked", self.hide_gui)
        toolbar.insert(open_button, 0)
        toolbar.insert(self.start_button, 1)
        #toolbar.insert(pause_button, 2)
        toolbar.insert(self.stop_button, 2)
        toolbar.insert(seperator, 3)
        toolbar.insert(json_button, 4)
        toolbar.insert(hide_button, 5)

        # Creating a Vertical Container To Add Widgets To
        vbox = gtk.VBox(False, 2)

        # Adding the Vertical Container To Main Window Frame
        self.add(vbox)
        self.connect("destroy", self.close_all)


        # Create File Menu Bar
        top_menu_bar = gtk.MenuBar()

        # Create menu that will be displayed in the GUI via the typical File drop down list
        filemenu = gtk.Menu()
        file_menu = gtk.MenuItem("File")
        file_menu.set_submenu(filemenu)

        # have to be appended in reverse order for some reason.
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", self.close_all)
        filemenu.append(exit)

        coreConfiguration = gtk.MenuItem("Core Configuration")
        coreConfiguration.connect("activate", Runner.call_core_config)
        filemenu.append(coreConfiguration)

        pluginConfiguration = gtk.MenuItem("Plugin Configuration")
        pluginConfiguration.connect("activate", Runner.call_plugins_config)
        filemenu.append(pluginConfiguration)

        top_menu_bar.append(file_menu)

        # Pack both Widgets on Screen
        vbox.pack_start(top_menu_bar, False, False, 0)
        vbox.pack_start(toolbar, False, False, 0)


        # Load Plugins On To Screen
        i=1
        for plugin in core.plugins:
            print "%d) %s" % (i, plugin.name)
            i = i+1
            vbox.pack_start(self.create_bbox(plugin),True, True, 5)

    # To be used by the status icon Main Application, it will bring the GUI back to the foreground
    def show_gui(self):
        self.show_all()

    # Will be accessed via the Hide Gui button.
    def hide_gui(self, event):
        self.hide()

    def parse_all(self, event, core):
        for plugin in core.plugins:
            core.parsers[plugin.name].parse()

    def create_bbox(self, plugin):
        layout = gtk.BUTTONBOX_SPREAD
        spacing = 10
        frame = gtk.Frame(plugin.name)

        bbox = gtk.HButtonBox()
        bbox.set_border_width(1)
        frame.add(bbox)

        # Get value of plugin "enabled status" from the associated json file.
        # hard coded right now, I want to have the "title" from the parameter be used for the path\config.json

        # Set the appearance of the Button Box
        bbox.set_layout(layout)
        bbox.set_spacing(spacing)


        enableButton = gtk.Button(str(plugin.is_enabled))
        enableButton.connect("clicked", self.enableButton_clicked)
        bbox.add(enableButton)

        parseButton = gtk.Button('Parse')
        parseButton.connect("clicked", self.parser, plugin.name)
        bbox.add(parseButton)


        if plugin.name == PYKEYLOGGER:
            appConfigButton = gtk.Button('Application Configuration')
            appConfigButton.connect("clicked", self.open_control_panel, plugin)
            bbox.add(appConfigButton)
        else:
            appConfigButton = gtk.Button('Application Configuration')
            appConfigButton.set_sensitive(False)
            bbox.add(appConfigButton)


        return frame

    def enableButton_clicked(self, button):
        print button.get_label()
        if button.get_label() == "Enabled":
            button.set_label("Disabled")


    def start_plugin(self, button):
        button.set_sensitive(False)
        self.stop_button.set_sensitive(True)
        for plugin in self.core.plugins:
            if plugin.is_enabled:
                plugin.run()


    def stop_plugin(self, button):
        self.start_button.set_sensitive(True)
        button.set_sensitive(False)
        for plugin in self.core.plugins:
            if plugin.is_enabled:
               plugin.terminate()

    def pause_plugin(self, button):
        for plugin in self.core.plugins:
            if plugin.suspend():
                plugin.resume()
            else:
                plugin.suspend()

    def close_all(self, event):
        os._exit(0)


    def parser(self, event, *args):
        self.core.parsers[args[0]].parse()

    def open_control_panel(self, event, plugin):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        if os.name == 'nt':
            subprocess.call(os.path.join(plugin.base_dir, "cpopen.bat"))
            #changes
        elif os.name == 'posix':
            subprocess.call(os.path.join(plugin.base_dir, "cpopen.sh"))
        else:
            print "Unknown OS"

    def callback(self, widget, data=None):
        filechooser = gtk.FileChooserDialog('Select Plugin Directory', None,
                                            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                            ('Cancel', 1, 'Open', 2))
        ans = filechooser.run()
        if ans == 2:
            new_plugin_path = os.path.normpath(filechooser.get_current_folder())
            folder = os.path.basename(new_plugin_path)
            if os.name == 'nt':
                shutil.copytree(new_plugin_path, os.path.join(os.getcwd(), "plugins\\collectors\\" + folder))
            elif os.name == 'posix':
                shutil.copytree(new_plugin_path, os.path.join(os.getcwd(), "plugins//collectors//" + folder))
            filechooser.destroy()
        else:
            filechooser.destroy()


    def copy(src, dst, event):
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))
        shutil.copytree(src, dst)

