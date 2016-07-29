import threading

def run(action, duration=0, music=None, set_wait_id=None, **kwargs):
    if set_wait_id is not None:
        action.mapping.add_wait_id(set_wait_id, action)

    action.sleep_event = threading.Event()
    action.sleep_event_timer = threading.Timer(
            duration,
            action.sleep_event.set)

    if music is not None:
        music.wait_end()

    action.sleep_event_timer.start()
    action.sleep_event.wait()

def description(action, duration=0, music=None, set_wait_id=None, **kwargs):
    formats = []
    message = ""
    if music is None:
        message += "waiting {}s"
        formats.append(duration)
    elif duration == 0:
        message += "waiting the end of « {} »"
        formats.append(music.name)
    else:
        message += "waiting the end of « {} » + {}s"
        formats.append(music.name)
        formats.append(duration)

    if set_wait_id is not None:
        message += " (setting id = {})"
        formats.append(set_wait_id)

    return _(message).format(*formats)

def interrupt(action, duration=0, music=None, **kwargs):
    if action.sleep_event is not None:
        action.sleep_event.set()
        action.sleep_event_timer.cancel()
    if music is not None:
        music.wait_event.set()
