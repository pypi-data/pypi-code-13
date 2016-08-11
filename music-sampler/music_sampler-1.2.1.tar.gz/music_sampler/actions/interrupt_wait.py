def run(action, wait_id=None, **kwargs):
    action.mapping.interrupt_wait(wait_id)

def description(action, wait_id=None, **kwargs):
    return _("interrupt wait with id {}").format(wait_id)
