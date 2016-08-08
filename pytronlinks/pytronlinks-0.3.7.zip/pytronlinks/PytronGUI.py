import wx
import client as Ai

TRAY_TOOLTIP = 'Pytron'
TRAY_ICON = 'icons/icon.ico'
SPLASH = 'images/splash.gif'


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        self.create_menu_item(menu, 'Settings', self.on_hello)
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def create_menu_item(self, menu, label, func):
        item = wx.MenuItem(menu, -1, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.AppendItem(item)
        return item

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        self.CreatePopupMenu()

    def on_hello(self, event):
        print 'Hello, world!'

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):

    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        self._show_splash()
        return True

    def _show_splash(self):
        # create, show and return the splash screen
        bitmap = wx.Bitmap(SPLASH)
        splash = wx.SplashScreen(bitmap, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 3000, None,
                                 style=wx.SIMPLE_BORDER | wx.STAY_ON_TOP)
        splash.Show()
        return splash


def main():
    Jarvis = Ai.Client()
    app = App(False)
    app.MainLoop()

if __name__ == '__main__':
    main()

