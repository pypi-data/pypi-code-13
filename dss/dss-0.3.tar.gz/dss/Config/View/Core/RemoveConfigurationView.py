import json
import os.path
from Tkinter import *
import DynamicView


class RemoveConfigurationView:
    def __init__(self, root, base_dir, config_file_name):
        self.root = root
        self.base_dir = base_dir
        self.config_file_name = config_file_name
        self.file_path = os.path.join(self.base_dir, 'core', self.config_file_name)

        self.top = Toplevel()
        self.top.title("Remove Field")
        self.top.minsize(width=350, height=150)

        self.keys = {}

        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                data = json.load(data_file)

                self.keys = data['General'].keys() + data['Archiving'].keys()

        self.selected_config = StringVar(self.top)
        self.selected_config.set(self.keys[0])

        plugin_dropdown_list = apply(OptionMenu, (self.top, self.selected_config) + tuple(self.keys))
        plugin_dropdown_list.grid(sticky="W", row=0)

        button_add = Button(self.top, text="Remove", command=self.remove_configuration)
        button_add.grid(sticky="W", row=1)

        button_close = Button(self.top, text="Close", command=self.top.destroy)
        button_close.grid(sticky="W", row=1, column=1)

    def remove_configuration(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path) as data_file:
                data = json.load(data_file)

                if self.selected_config.get() in data['General']:
                    del data['General'][self.selected_config.get()]
                else:
                    del data['Archiving'][self.selected_config.get()]

                with open(self.file_path, 'w') as outfile:
                    json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

            remove_labels_and_entries(self.root)
            DynamicView.MakeView(self.root, self.base_dir, self.config_file_name)

            self.top.destroy()


def remove_labels_and_entries(root):
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
