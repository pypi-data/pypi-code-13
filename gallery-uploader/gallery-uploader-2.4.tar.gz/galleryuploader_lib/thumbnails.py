from threading import Thread
from gnome import ui
from gtk import gdk
import os
import time, gio


class Thumbnailer(Thread):
    def __init__(self, basedir='.'):
        Thread.__init__(self)
        self.daemon = True
        self.go = True
        self.todo = []
        self.done = []
        self.basedir = basedir
        # iff not self.todo and not self.working, then it is guaranteed that
        # self.done won't grow (until self.todo isn't filled again)
        self.working = False
        self.thumbFactory = ui.ThumbnailFactory(ui.THUMBNAIL_SIZE_NORMAL)
    
    def reset(self, todo, basedir='.'):
        self.res = False
        self.done = []
        self.todo = todo
        self.basedir = basedir

    def run(self):
        while self.go:
            self.res = False
            if self.todo:
                self.working = True
                thing = self.todo.pop(0)
                handler = gio.File( os.path.join( self.basedir, thing ) )
                info = handler.query_info('*')
                mime = info.get_content_type()

                if mime.startswith('image') or mime.startswith('video'):
                    thumbnail = None
                    uri = handler.get_uri()

                    existing = self.thumbFactory.lookup( uri, 0 )
                    if existing:
                        thumbnail = gdk.pixbuf_new_from_file( existing )
                    elif not self.thumbFactory.has_valid_failed_thumbnail( uri, 0 )\
                         and self.thumbFactory.can_thumbnail(uri, mime, 0):
                            thumbnail = self.thumbFactory.generate_thumbnail(uri, mime)
                else:
                    continue

                if thumbnail != None:
                    self.thumbFactory.save_thumbnail(thumbnail, uri, 0)
                    if not self.res:
                        self.done.append((thing, uri, thumbnail))
                self.working = False
            else:
                time.sleep(.2)
