import os, gobject, sys, pango
import gtk
from thumbnails import Thumbnailer
from dialogs import build_builder

class Editor(object):
    """
    This handles the dialog in which image properties (currently, captions and
    descriptions) can be edited before uploading.
    """
    def __init__(self):
        self.dialog_builder = build_builder( 'edit' )
        self.dialog = self.dialog_builder.get_object( 'dialog' )
        self.list = self.dialog_builder.get_object( 'list' )
        self.tree = self.dialog_builder.get_object( 'tree' )
        
        col = gtk.TreeViewColumn()
        rend = gtk.CellRendererPixbuf()
        rend.set_property( 'stock-size', 3 )
        col.pack_start( rend )
        col.add_attribute( rend, 'pixbuf', 3 )
        self.tree.append_column( col )
        
        text_fields = [('Name',        4, {}                            ),
                       ('Caption',     1, {'wrap-mode'  : pango.WRAP_WORD,
                                           'wrap-width' : 100,
                                           'editable'   : True}         ),
                       ('Description', 2, {'wrap-mode'  : pango.WRAP_WORD,
                                           'wrap-width' : 180,
                                           'editable'   : True}         )]
        
        for index in range(3):
            field, col_numb, properties = text_fields[index]
            col = gtk.TreeViewColumn( field )
            rend = gtk.CellRendererText()
            for prop in properties:
                rend.set_property( prop, properties[prop] )
            if 'editable' in properties:
                rend.connect( 'edited', self.edited, col_numb )
            col.pack_start( rend )
            col.add_attribute( rend, 'text', col_numb )
            self.tree.append_column( col )
        
        self.thumbnailer = Thumbnailer()
        self.thumbnailer.start()
        self.alive = True
        gobject.timeout_add(100, self.monitor)
    
    def run(self, files):
        """
        Start the dialog.
        """
        self.thumbnailer.todo = list( files )
        resp = self.dialog.run()
        self.thumbnailer.go = False
        self.dialog.hide()
        if resp:
            # TODO: don't quit, go back to last step!
            sys.exit( 0 )
        else:
            return [list( row )[:3] for row in self.list]

    def destroy(self):
        """
        Close the dialog.
        """
        self.alive = False
        self.dialog.hide()
    
    def edited(self, cellrenderer, row, content, column):
        """
        Save modified text field.
        """
        self.list[row][column] = content
    
    def monitor(self):
        """
        This is ran as long as the thumbnailer is working.
        """
        # If we see the thumbnailer has finished working...
        finished = bool( self.thumbnailer.todo ) or self.thumbnailer.working
        # ... _and then_ we get all the "done" thumbnails...
        while self.thumbnailer.done:
            path, uri, thumbnail = self.thumbnailer.done.pop(0)
            self.list.append([path,
                              '',
                              '',
                              thumbnail,
                              os.path.basename( path )])
        # ... then we know we're missing none.
        return finished
