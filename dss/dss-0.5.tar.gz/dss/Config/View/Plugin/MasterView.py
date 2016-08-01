import os.path
from Tkinter import *
from Config.View.Plugin import DynamicView


class MakePluginsView:
    def __init__(self, base_dir, config_file_name):
        self.base_dir = base_dir
        self.config_file_name = config_file_name
        self.plugin_names = [directory for directory in os.listdir(os.path.join(base_dir, 'plugins', 'collectors')) if
                             os.path.isdir(os.path.join(base_dir, 'plugins', 'collectors', directory))]

        root = Tk()

        label_plugins = Label(root, text="Plugins")

        selected_plugin = StringVar(root)
        selected_plugin.set(self.plugin_names[0])

        plugin_dropdown_list = apply(OptionMenu, (root, selected_plugin) + tuple(self.plugin_names))

        DynamicView.MakeView(root, self.base_dir, self.plugin_names[0], self.config_file_name)

        def select_plugin():
            remove_labels_and_entries()
            DynamicView.MakeView(root, self.base_dir, selected_plugin.get(), self.config_file_name)

        button_select_plugin = Button(root, text="Select Plugin", command=select_plugin)
        button_close = Button(root, text="Close", command=root.destroy)

        label_plugins.grid(sticky="W", row=0)
        plugin_dropdown_list.grid(sticky="W", row=1)
        button_select_plugin.grid(sticky="W", row=2)
        button_close.grid(sticky="W", row=3)

        def remove_labels_and_entries():
            for label in root.grid_slaves():
                if int(label.grid_info()["column"]) == 1:
                    label.grid_forget()
            for field in root.grid_slaves():
                if int(field.grid_info()["column"]) == 1:
                    field.grid_forget()
            for label in root.grid_slaves():
                if int(label.grid_info()["column"]) == 2:
                    label.grid_forget()
            for field in root.grid_slaves():
                if int(field.grid_info()["column"]) == 2:
                    field.grid_forget()

        root.minsize(width=500, height=250)
        root.wm_title("Configure Plugin Settings")
        mainloop()
