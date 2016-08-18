import os, gobject, gio
from itertools import count
from galleryuploader_lib.thumbnails import Thumbnailer
from galleryuploader_lib.dialogs import build_builder

class Browser(object):
    new_id = count().next
    def __init__(self):
        self.dialog_builder = build_builder('browser')
        self.dialog = self.dialog_builder.get_object('dialog')
        self.list = self.dialog_builder.get_object('list')
        self.icons = self.dialog_builder.get_object('icons')
        self.filechooser = self.dialog_builder.get_object('filechooser')
        self.icons.set_text_column(1)
        self.icons.set_pixbuf_column(2)
                
        self.current_folder = gio.File('.').get_path()
#        print "self.current_folder", self.current_folder
        self.thumbnailer = Thumbnailer()
        self.thumbnailer.start()
        self.populate()
        self.alive = True
        gobject.timeout_add(100, self.monitor)
    
    def run(self):
        resp = self.dialog.run()
        self.thumbnailer.go = False
        if resp:
            return self.get_filenames()
        else:
            return None

    def destroy(self):
        self.alive = False
        self.dialog.destroy()
    
    def get_filenames(self):
        """
        Retrieve paths corresponding to selected thumbnails.
        """
        retval = []

        def iterator(iconview, path, *args):
            full_path = os.path.join( os.path.realpath( os.curdir ),
                           self.list.get_value(self.list.get_iter( path ), 1 ) )
            retval.append( full_path )

        self.icons.selected_foreach( iterator )
        return retval

    def populate(self):
        self.list.clear()
        curdir = os.path.realpath( os.curdir )
        dir_content = os.listdir( curdir )
        dir_content.sort()
        self.thumbnailer.reset(dir_content, basedir=curdir)
        
    def monitor(self):
        if self.alive == False:
            return False
    
        if not self.filechooser.get_filename():
            return True

        if self.current_folder != self.filechooser.get_filename():
            self.current_folder = self.filechooser.get_filename()
            os.chdir(self.current_folder)
            self.populate()
            return True

        while self.thumbnailer.done:
            thing, uri, thumbnail = self.thumbnailer.done.pop(0)
            self.list.append([self.new_id(), thing, thumbnail])

        return True
