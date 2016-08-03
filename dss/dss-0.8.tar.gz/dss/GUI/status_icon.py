# For GUI
import os
import gtk
# For Screen Capture
import autopy
from plugins.collectors.manualscreenshot import takeshoot


class CustomSystemTrayIcon:

    def __init__(self, core, gui):
        self.gui = gui
        self.core = core
        self.tray = gtk.StatusIcon()
        self.tray.set_from_stock(gtk.STOCK_ABOUT)
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.set_tooltip(('Decision Support System Logger V 1.0'))


    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time)

    def make_menu(self, event_button, event_time):
        menu = gtk.Menu()

        # show main application
        about = gtk.MenuItem("Main Application")
        about.show()
        menu.append(about)
        about.connect('activate', self.show_my_gui, self.gui)

        # show about dialog
        about = gtk.MenuItem("About")
        about.show()
        menu.append(about)
        about.connect('activate', self.show_about_dialog)

        # add manual screenshot functionality
        screen_shot = gtk.MenuItem("Take Manual ScreenShot")
        ms = self.core.get_plugin("manualscreenshot")
        if ms.is_enabled:
            screen_shot.show()
            menu.append(screen_shot)
            screen_shot.connect("activate", self.takeScreen)
        #screen_shot.connect("activate", t)


        # add quit item
        quit = gtk.MenuItem("Quit")
        quit.show()
        menu.append(quit)
        quit.connect('activate', self.kill_me)

        menu.popup(None, None, gtk.status_icon_position_menu,
                   event_button, event_time, self.tray)

    # Simple pop up widget that shows some information about the program
    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_icon_name("Decision Support System Logger V 1.0")
        about_dialog.set_name('DSS')
        about_dialog.set_version('1.0')
        about_dialog.set_comments(("Practicum Fall 2016"))
        about_dialog.run()
        about_dialog.destroy()

    def takeScreen(event_button, event):
        takeshoot.CaptureScreen()
        #CustomSystemTrayIcon.core1.get_plugin("manualscreenshot").run()

    def kill_me(self, event):
        for plugin in self.core.plugins:
            if plugin.is_enabled:
               plugin.terminate()
        os._exit(0)

    def show_my_gui(self, event, gui):
        gui()
