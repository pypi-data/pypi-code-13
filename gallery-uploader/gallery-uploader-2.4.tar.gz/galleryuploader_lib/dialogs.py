import gtk
from config import *

########################## DIALOGS #############################################

def build_builder(name):
    try:
        builder = gtk.Builder()
        builder.set_translation_domain(APP)
        builder.add_from_file(STUFF_DIR + '/UI_' + name + '.glade')
        return builder
    except Exception, err:
        fatal_error( err )

def fatal_error(err):
    """
    Used for any error that makes gallery-uploader exit.
    """
    err = (_('Gallery-uploader is exiting because of the following error:'),) + tuple( err )

    try:
        error_dialog( *err )
    except RuntimeError:
        print '\n'.join( err )
    sys.exit( 1 )

def chooser(title, text):
    dialog_builder = build_builder('choose')
    dialog = dialog_builder.get_object('dialog')
    dialog.set_title(title)
    label = dialog_builder.get_object('label')
    label.set_text(text)
    tree = dialog_builder.get_object('tree')

    
    def check_validity(selection, sensitives):
        for button in sensitives:
            button.set_sensitive(bool(selection.get_selected()[1]))
    
    sensitives = [dialog_builder.get_object(name) for name in ('ok', 'delete', 'edit', 'new_album')]
   
    selection = tree.get_selection()

    selection.connect('changed', check_validity, sensitives)
    
    interesting = ('new', 'delete', 'edit', 'expand', 'collapse', 'accounts', 'new_album')
    
    return dialog, tree, dict(zip(interesting, [dialog_builder.get_object(name) for name in interesting]))

def areyousurer(text, parent=None):
    dialog_builder = build_builder('delete')
    dialog = dialog_builder.get_object('dialog')
    dialog.set_transient_for(parent)
    dialog.set_markup(text)
    return dialog

def error_dialog(message, text, debug=True):
    """
    """
    dialog_builder = build_builder('error')
    dialog = dialog_builder.get_object('dialog')
    dialog.set_markup(message)
    if debug:
        debug_buffer = dialog_builder.get_object('debug_buffer')
        debug_buffer.set_text(text)
    else:
        debug_area = dialog_builder.get_object('debug_area')
        debug_area.hide()
        text_label = dialog_builder.get_object('text_label')
        text_label.set_text(text)

    # FIXME: temporary? See http://bugzilla.gnome.org/show_bug.cgi?id=587901
    dialog.set_skip_taskbar_hint(False)

    dialog.run()
    dialog.hide()

########################## END OF DIALOGS ######################################
